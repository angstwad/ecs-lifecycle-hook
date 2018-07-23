import logging
import os
import uuid

import botocore
import pytest

import fixtures
import handler
import exc


@pytest.fixture
def instance():
    inst = handler.Instance('testInstance')
    inst.id = fixtures.container_instance_draining['ec2InstanceId']
    return inst


@pytest.fixture
def node():
    return handler.EcsNode(cluster(), fixtures.container_instance_draining)


@pytest.fixture
def cluster():
    return handler.EcsCluster('TestCluster')


@pytest.fixture
def sns_topic(mocker):
    return mocker.Mock()


def test_log_level():
    handler.setup_logger()
    assert handler.logger.level is logging.WARNING

    os.environ['LOGLEVEL'] = 'DEBUG'
    handler.setup_logger()
    assert handler.logger.level is logging.DEBUG


def test_AutoScalingGroup(mocker):
    mocker.patch('handler.asg.complete_lifecycle_action')

    # __init__
    asg = handler.AutoScalingGroup('foobar')
    assert asg.name == 'foobar'

    asg.terminate('token', 'hook_name', action='FOOBAR')
    handler.asg.complete_lifecycle_action.assert_called_once_with(
        AutoScalingGroupName='foobar',
        LifecycleActionResult='FOOBAR',
        LifecycleActionToken='token',
        LifecycleHookName='hook_name'
    )


def test_Instance(mocker):
    mocker.patch('handler.ec2.Instance')

    # __init__
    inst = handler.Instance('foobar')
    handler.ec2.Instance.assert_called_once_with('foobar')

    # check class properties
    inst.tags = [{'Key': 'Name', 'Value': 'foobarcluster ECS host'}]
    assert inst.name == 'foobarcluster ECS host'
    assert inst.cluster_name == 'foobarcluster'
    assert inst.is_ecs_cluster_node is True

    inst.tags = [{'Key': 'Name', 'Value': 'foobarcluster'}]
    assert inst.cluster_name is None
    assert inst.is_ecs_cluster_node is False


def test_Instance_bad_ec2_Instance(mocker):
    mocker.patch('handler.ec2.Instance')

    # This is bubbled up when the underlying ec2 instance doesn't exist
    handler.ec2.Instance.tags.side_effect = AttributeError
    inst = handler.Instance('foobar')

    # check class properties
    assert inst.name is None
    assert inst.cluster_name is None
    assert inst.is_ecs_cluster_node is False


def test_EcsNode(mocker, cluster):
    mocker.patch('handler.ecs.update_container_instances_state')
    node = handler.EcsNode(cluster, fixtures.container_instance_active)

    # test __getitem__
    with pytest.raises(KeyError):
        node['foo']
    assert node['containerInstanceArn']

    assert node.id == '4336ffad-f3af-41a3-b1f0-e20ba7db2c82'


def test_EcsNode_drain_active(mocker, cluster):
    mocker.patch('handler.ecs.update_container_instances_state')
    node = handler.EcsNode(cluster, fixtures.container_instance_active)
    node.drain()
    handler.ecs.update_container_instances_state.assert_called_with(
        cluster='TestCluster',
        containerInstances=[node['containerInstanceArn']],
        status='DRAINING'
    )


def test_EcsNodeDrain_draining(mocker, cluster):
    mocker.patch('handler.ecs.update_container_instances_state')
    node = handler.EcsNode(cluster, fixtures.container_instance_draining)

    with pytest.raises(exc.EcsError):
        node.drain()


def test_EcsCluster_get_node(mocker, instance):
    mocker.patch('handler.ecs')
    handler.ecs.list_container_instances.return_value = fixtures.list_container_instances_response
    handler.ecs.describe_container_instances.return_value = fixtures.describe_container_instances_response  # noqa

    cluster_ = handler.EcsCluster('TestCluster')
    node = cluster_.get_node(instance)
    assert isinstance(node, handler.EcsNode)


def test_EcsCluster_get_tasks(mocker, node):
    mocker.patch('handler.ecs')
    handler.ecs.list_tasks.return_value = fixtures.list_tasks_response

    cluster = handler.EcsCluster('TestCluster')
    tasks = cluster.get_tasks(node)
    assert tasks == fixtures.list_tasks_response['taskArns']


def test_EcsCluster_stop_daemon_tasks(mocker, node):
    mocker.patch('handler.ecs')
    mocker.patch('handler.logger')
    handler.ecs.list_tasks.return_value = fixtures.list_tasks_response
    handler.ecs.describe_tasks.return_value = fixtures.describe_tasks_response

    cluster = handler.EcsCluster('TestCluster')
    cluster.stop_daemon_tasks(node)

    handler.ecs.stop_task.assert_called_once_with(
        cluster='TestCluster',
        task='this is a fake task ARN'
    )
    handler.logger.info.assert_called()

    # ecs.stop_task raises botocore.exceptions.ClientError
    handler.ecs.list_tasks.reset_mock()
    handler.ecs.stop_task.side_effect = botocore.exceptions.ClientError({}, {})

    cluster.stop_daemon_tasks(node)
    handler.logger.error.assert_called_once()


def test_EcsCluster_only_daemon_tasks_remaining(mocker, node):
    mocker.patch('handler.ecs')

    cluster = handler.EcsCluster('TestCluster')

    handler.ecs.describe_tasks.return_value = fixtures.describe_tasks_response_only_daemon_tasks
    assert cluster.only_daemon_tasks_remaining(node) is True

    handler.ecs.describe_tasks.return_value = fixtures.describe_tasks_response_mixed_startedby
    assert cluster.only_daemon_tasks_remaining(node) is False

    handler.ecs.describe_tasks.return_value = fixtures.describe_tasks_response_only_scheduled_tasks
    assert cluster.only_daemon_tasks_remaining(node) is False

    handler.ecs.describe_tasks.return_value = fixtures.describe_tasks_response_no_tasks
    assert cluster.only_daemon_tasks_remaining(node) is True


def test_lambda_handler_malformed_event(mocker):
    mocker.patch('handler.logger')
    mocker.patch('handler.run')

    assert handler.lambda_handler({}, None) is "error"


def test_lambda_handler_successful_run(mocker):
    mocker.patch('handler.logger')
    mocker.patch('handler.sns.Topic')
    mocker.patch('handler.run')

    topic = uuid.uuid4().hex
    handler.sns.Topic.return_value = topic
    handler.run.return_value = "ok"

    result = handler.lambda_handler(fixtures.termination_event, None)

    # check return result of run
    assert result == "ok"
    # check right arguments to run
    handler.run.assert_called_with(
        fixtures.termination_event['Records'][0]['Sns'],
        topic
    )


def test_lambda_handler_run_with_exception(mocker):
    mocker.patch('handler.run')
    mocker.patch('handler.sns')

    mock_topic = mocker.Mock()
    handler.sns.Topic.return_value = mock_topic

    exc = Exception('foobar')
    handler.run.side_effect = exc

    result = handler.lambda_handler(fixtures.termination_event, None)

    # check republishing of event on exception
    mock_topic.publish.assert_called_once()
    # check handler returns "error"
    assert result == "error"


def test_run_message_body_bad_json():
    with pytest.raises(exc.JsonDecodeError):
        handler.run({'Message': ''}, None)


def test_run_not_lifecycle_hook(sns_topic):
    result = handler.run(fixtures.non_lifecycle_message_json, sns_topic)
    assert result == 'error'


def test_run_not_cluster_node(mocker, sns_topic):
    mocker.patch('handler.EcsCluster')
    mocker.patch('handler.logger')
    mocker.patch('handler.Instance')

    mock = mocker.Mock()
    mock.is_ecs_cluster_node = False
    handler.Instance.return_value = mock

    resp = handler.run(fixtures.termination_message_json, sns_topic)

    assert resp == "error"
    handler.logger.error.assert_called_once()
    assert not handler.EcsCluster.called


def test_run_has_daemon_tasks(mocker, sns_topic):
    mocker.patch('handler.EcsCluster')
    mocker.patch('handler.logger')
    mocker.patch('handler.Instance')
    mocker.patch('handler.AutoScalingGroup')
    mocker.patch('handler.time.sleep')

    mock_node = mocker.Mock()
    mock_node.drain.side_effect = exc.EcsError('foobar')
    mock_node.__getitem__ = lambda x, y: 1

    mock_cluster = mocker.Mock()
    mock_cluster.get_node.return_value = mock_node
    mock_cluster.only_daemon_tasks_remaining.return_value = True

    handler.EcsCluster.return_value = mock_cluster

    resp = handler.run(fixtures.termination_message_json, sns_topic)

    assert resp == 'ok'
    handler.time.sleep.assert_called_once()
    mock_cluster.stop_daemon_tasks.assert_called_once()
    sns_topic.publish.assert_called_once()
    assert handler.AutoScalingGroup.call_count is 0


def test_lambda_no_tasks(mocker, sns_topic):
    mocker.patch('handler.EcsCluster')
    mocker.patch('handler.logger')
    mocker.patch('handler.Instance')
    mocker.patch('handler.AutoScalingGroup')
    mocker.patch('handler.time.sleep')

    mock_node = mocker.Mock()
    mock_node.drain.side_effect = exc.EcsError('foobar')
    mock_node.__getitem__ = lambda x, y: 0

    mock_cluster = mocker.Mock()
    mock_cluster.get_node.return_value = mock_node

    mock_asg = mocker.Mock()
    handler.AutoScalingGroup.return_value = mock_asg

    handler.EcsCluster.return_value = mock_cluster

    resp = handler.run(fixtures.termination_message_json, sns_topic)

    assert resp == 'ok'
    handler.time.sleep.assert_not_called()
    mock_asg.terminate.assert_called_once_with(
        '86799385-e46d-40b9-a393-6ff3da981d7e',
        'testing-ASGTerminateHook-11414UVQ4RWSR'
    )
