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

import json
import logging
import os
import re
import time

import boto3
from botocore.exceptions import ClientError
from trythatagain import retry_exp_backoff
from voluptuous import Schema, Invalid, ALLOW_EXTRA

from exc import EcsError, JsonDecodeError

_session = boto3.Session()
ecs = _session.client('ecs')
ec2 = _session.resource('ec2')
sns = _session.resource('sns')
asg = _session.client('autoscaling')
logger = None

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
        logger.info(f'Completing lifecycle with action {action}')
        logger.debug('Lifecycle action token %s', token)
        logger.debug('Lifecycle hook name %s', hook_name)
        resp = asg.complete_lifecycle_action(
            LifecycleActionToken=token,
            LifecycleActionResult=action,
            LifecycleHookName=hook_name,
            AutoScalingGroupName=self.name
        )
        logger.debug('Colplete lifecycle action resp: %s', resp)


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
        logger.info(f'Checking if instance {self.id} belongs to ECS cluster')
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
        logger.info(f'Draining node {self.id}')
        if self['status'] == 'ACTIVE':
            resp = ecs.update_container_instances_state(
                cluster=self._cluster.name,
                containerInstances=[self['containerInstanceArn']],
                status='DRAINING'
            )
            logger.debug('Update container inst state resp: %s', resp)
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
        logger.info(f'Getting ECS node for instance {instance.id}')

        list_resp = ecs.list_container_instances(
            cluster=self.name
        )
        logger.debug('List container instances resp %s', list_resp)
        desc_resp = ecs.describe_container_instances(
            cluster=self.name,
            containerInstances=list_resp['containerInstanceArns']
        )
        logger.debug('Describe container instances resp %s', desc_resp)

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
        logger.info(f'Stopping daemon tasks on node {node.id}')
        tasks = self.get_tasks(node)

        if tasks:
            desc_tasks_resp = ecs.describe_tasks(
                cluster=self.name,
                tasks=tasks
            )

            logger.debug('Describe tasks resp: %s', desc_tasks_resp)

            for task in desc_tasks_resp['tasks']:
                if task['startedBy'] == node.id:
                    logger.info(f'Task {task["group"]} started by '
                                'instance, stopping...')
                    try:
                        ecs.stop_task(cluster=self.name, task=task['taskArn'])
                    except ClientError:
                        logger.error(f"Couldn't find task {task['taskArn']}")

    def only_daemon_tasks_remaining(self, node):
        logger.info(f'Checking if only daemon tasks remain on node {node.id}')
        tasks = self.get_tasks(node)

        results = []

        if tasks:
            desc_tasks_resp = ecs.describe_tasks(
                cluster=self.name,
                tasks=tasks
            )

            logger.debug('Describe tasks resp: %s', desc_tasks_resp)

            for task in desc_tasks_resp['tasks']:
                if task['startedBy'] == node.id:
                    results.append(True)
                else:
                    results.append(False)

        return all(results)


def setup_logger():
    global logger
    logging.basicConfig()
    logger = logging.getLogger('lifecycle_hook')
    loglevel = os.environ.get('LOGLEVEL', 'WARNING')
    logger.setLevel(getattr(logging, loglevel))
    logger.info(f'Set lambda log level to {loglevel}')

    # this adjusts boto3 log level
    root_logger = logging.getLogger()
    root_loglevel = os.environ.get('ROOT_LOGLEVEL', 'WARNING')
    root_logger.setLevel(getattr(logging, root_loglevel))
    logger.info(f'Set root log level to {root_loglevel}')


@retry_exp_backoff(retries=10, raise_for=JsonDecodeError)
def run(sns_message, sns_topic):
    logger.info('Processing event')

    sleep_time = round(abs(int(os.environ.get('SLEEP_MS', 0)) / 1000), 1)
    logger.debug(f'Configured sleep time is {sleep_time} seconds')

    try:
        logger.info('JSON decoding SNS message')
        message = sns_message['Message']
        logger.debug(message)
        message_body = json.loads(message)
    except ValueError as e:
        raise JsonDecodeError(f'Could not JSON decode SNS message: {e}')

    # check if it's a lifecycle hook
    try:
        logger.info('Checking if SNS message is a lifecycle hook')
        lifecycle_hook_schema(message_body)
    except Invalid as e:
        logger.info('Message was not a lifecycle hook')
        logger.info(e)
        return "error"

    inst = Instance(message_body['EC2InstanceId'])

    if not inst.is_ecs_cluster_node:
        logger.error(f'Instance {inst.id} does not belong to a cluster')
        return "error"
    else:
        logger.info(f'Instance {inst.id} node belongs to ECS cluster')

    cluster = EcsCluster(inst.cluster_name)
    node = cluster.get_node(inst)

    if not node:
        logger.error(f'Cluster {cluster.name} does not contain {inst.id}')
        return "error"

    try:
        node.drain()
    except EcsError as e:
        # node is already draining
        logger.info(e)

    # stop daemon takss after all other tasks have been stopped
    if cluster.only_daemon_tasks_remaining(node):
        cluster.stop_daemon_tasks(node)

    node = cluster.get_node(inst)

    if node['runningTasksCount'] != 0:
        # publish message to SNS topic
        logger.info(
            f'Instance {inst.id} still has running tasks; '
            f'republishing message.'
        )

        if sleep_time:
            logger.info(f'Sleeping for {sleep_time} seconds')
        time.sleep(sleep_time)

        sns_topic.publish(
            Subject=sns_message['Subject'],
            Message=sns_message['Message'],
        )

        return "ok"

    logger.info(f'All tasks on {cluster.name} are stopped')
    logger.info(f'Completing lifecycle for {inst.id}')
    asg = AutoScalingGroup(message_body['AutoScalingGroupName'])
    asg.terminate(message_body['LifecycleActionToken'],
                  message_body['LifecycleHookName'])

    return "ok"


def lambda_handler(event, context):
    setup_logger()

    try:
        logger.info('Validating incoming event schema')
        logger.debug(json.dumps(event, indent=2))
        event_schema(event)
    except Invalid as e:
        logger.error('Malformed event')
        logger.error(e)
        logger.error(event)
        return "error"
    else:
        logger.info('Incoming event validated')

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
