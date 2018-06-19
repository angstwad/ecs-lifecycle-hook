# -*- coding: utf-8 -*-
# Copyright 2018 Paul Durivage <pauldurivage+github@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
import os
import re

import boto3
from botocore.exceptions import ClientError
from voluptuous import Schema, Invalid, ALLOW_EXTRA
from trythatagain import retry_exp_backoff

from exc import EcsError, JsonDecodeError

_session = boto3.Session()
ecs = _session.client('ecs')
ec2 = _session.resource('ec2')
sns = _session.resource('sns')
asg = _session.client('autoscaling')

logger = logging.getLogger()
logger.setLevel(getattr(logging, os.environ.get('LOGLEVEL', 'INFO')))

event_schema = Schema({
    'Records': Schema([
        {
            'Sns': {
                'TopicArn': str,
                'Message': str,
            }
        }
    ], required=True, extra=ALLOW_EXTRA)
}, required=True, extra=ALLOW_EXTRA)

lifecycle_hook_schema = Schema({
    'AutoScalingGroupName': str,
    'EC2InstanceId': str,
    'LifecycleActionToken': str,
    'LifecycleHookName': str,
    'LifecycleTransition': 'autoscaling:EC2_INSTANCE_TERMINATING',
}, required=True, extra=ALLOW_EXTRA)


class AutoScalingGroup(object):
    def __init__(self, name):
        self.name = name

    def terminate(self, token, hook_name, action='CONTINUE'):
        asg.complete_lifecycle_action(
            LifecycleActionToken=token,
            LifecycleActionResult=action,
            LifecycleHookName=hook_name,
            AutoScalingGroupName=self.name
        )


class Instance(object):
    def __init__(self, id):
        self._instance = ec2.Instance(id)

    def __getattr__(self, item):
        try:
            return getattr(self._instance, item)
        except ClientError as e:
            raise AttributeError(
                f'Unable to fetch underlying instance attributes: {e}'
            )

    @property
    def name(self):
        try:
            for tag in self.tags:
                if tag['Key'] == 'Name':
                    return tag['Value']
        except AttributeError:
            pass

    @property
    def cluster_name(self):
        match = re.search('^(.*) ECS host$', self.name or '')
        if match:
            return match.group(1)

    @property
    def is_ecs_cluster_node(self):
        if self.cluster_name is not None:
            return True
        return False


class EcsNode(object):
    def __init__(self, cluster, data):
        self._cluster = cluster
        self._data = data

    def __getitem__(self, item):
        return self._data[item]

    def drain(self):
        if self['status'] == 'ACTIVE':
            ecs.update_container_instances_state(
                cluster=self._cluster.name,
                containerInstances=[self['containerInstanceArn']],
                status='DRAINING'
            )
        else:
            raise EcsError('Node status not ACTIVE')

    @property
    def id(self):
        return self['containerInstanceArn'].split('/')[1]


class EcsCluster(object):
    def __init__(self, cluster_name):
        self.name = cluster_name
        self.terminating_node = None

    def get_node(self, instance):
        list_resp = ecs.list_container_instances(
            cluster=self.name
        )
        desc_resp = ecs.describe_container_instances(
            cluster=self.name,
            containerInstances=list_resp['containerInstanceArns']
        )

        for node in desc_resp['containerInstances']:
            if node['ec2InstanceId'] == instance.id:
                self.terminating_node = EcsNode(self, node)
                break

        return self.terminating_node

    def get_tasks(self, node):
        return ecs.list_tasks(
            cluster=self.name,
            containerInstance=node.id
        )['taskArns']

    def stop_daemon_tasks(self, node):
        tasks = self.get_tasks(node)

        if tasks:
            desc_tasks_resp = ecs.describe_tasks(
                cluster=self.name,
                tasks=tasks
            )

            for task in desc_tasks_resp['tasks']:
                if task['startedBy'] == node.id:
                    logger.info(f'Task {task["group"]} started by '
                                'instance, stopping...')
                    try:
                        ecs.stop_task(cluster=self.name, task=task['taskArn'])
                    except ClientError:
                        logger.error(f"Couldn't find task {task['taskArn']}")

    def only_daemon_tasks_remaining(self, node):
        tasks = self.get_tasks(node)

        results = []

        if tasks:
            desc_tasks_resp = ecs.describe_tasks(
                cluster=self.name,
                tasks=tasks
            )

            for task in desc_tasks_resp['tasks']:
                if task['startedBy'] == node.id:
                    results.append(True)
                else:
                    results.append(False)

        return all(results)


@retry_exp_backoff(retries=10)
def run(sns_message, sns_topic):
    try:
        message_body = json.loads(sns_message['Message'])
    except ValueError as e:
        raise JsonDecodeError(f'Could not JSON decode SNS message: {e}')

    # check if it's a lifecycle hook
    try:
        lifecycle_hook_schema(message_body)
    except Invalid as e:
        logger.debug('Message was not a lifecycle hook')
        logger.debug(e)
        return "error"

    inst = Instance(message_body['EC2InstanceId'])

    if not inst.is_ecs_cluster_node:
        logger.error(f'Instance {inst.id} does not belong to a cluster')
        return "error"

    cluster = EcsCluster(inst.cluster_name)
    node = cluster.get_node(inst)

    if not node:
        logger.error(f'Cluster {cluster.name} does not contain {inst.id}')
        return "error"

    try:
        node.drain()
    except EcsError as e:
        # node is already draining
        logger.debug(e)

    # stop daemon takss after all other tasks have been stopped
    if cluster.only_daemon_tasks_remaining(node):
        cluster.stop_daemon_tasks(node)

    node = cluster.get_node(inst)

    if node['runningTasksCount'] != 0:
        # publish message to SNS topic
        logger.debug(
            f'Instance {inst.id} still has running tasks; '
            f'republishing message.'
        )
        sns_topic.publish(
            Subject=sns_message['Subject'],
            Message=sns_message['Message'],
        )
        return "ok"

    logger.debug(f'All tasks on {cluster.name} are stopped')
    logger.debug(f'Completing lifecycle for {inst.id}')
    asg = AutoScalingGroup(message_body['AutoScalingGroupName'])
    asg.terminate(message_body['LifecycleActionToken'],
                  message_body['LifecycleHookName'])

    return "ok"


def lambda_handler(event, context):
    try:
        event_schema(event)
    except Invalid as e:
        logger.error('Malformed event')
        logger.error(e)
        logger.error(event)
        return "error"

    topic_arn = event['Records'][0]['Sns']['TopicArn']
    sns_message = event['Records'][0]['Sns']

    sns_topic = sns.Topic(topic_arn)

    try:
        return run(sns_message, sns_topic)
    except Exception as e:
        logger.exception(f'Failed during execution: {e}', exc_info=True)
        sns_topic.publish(
            Subject=sns_message['Subject'],
            Message=sns_message['Message'],
        )
        return "error"

    return "ok"
