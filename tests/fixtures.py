import datetime

from dateutil.tz import tzlocal

termination_event = {
    'Records': [
        {
            'EventSource': 'aws:sns',
            'EventSubscriptionArn': 'arn:aws:sns:us-east-1:01234567890:ecs-lifecycle-hook:0ecad48e-b088-42eb-adf5-ff5cf998b276',
            'EventVersion': '1.0',
            'Sns': {
                'Type': 'Notification',
                'MessageId': '71f5932c-d579-5dfb-803d-c0470cce0537',
                'TopicArn': 'arn:aws:sns:us-east-1:01234567890:ecs-lifecycle-hook',
                'Subject': 'Auto Scaling:  Lifecycle action \'TERMINATING\' for instance i-01234567890abcdef in progress.',
                'Message': '{"LifecycleHookName":"testing-ASGTerminateHook-11414UVQ4RWSR","AccountId":"01234567890","RequestId":"6d182a89-b489-4116-b810-f73d3db5b477","LifecycleTransition":"autoscaling:EC2_INSTANCE_TERMINATING","AutoScalingGroupName":"testing-ECSAutoScalingGroup-J80BFBLVR4ZJ","Service":"AWS Auto Scaling","Time":"2018-05-08T16:59:35.661Z","EC2InstanceId":"i-01234567890abcdef","LifecycleActionToken":"86799385-e46d-40b9-a393-6ff3da981d7e"}',
                'Timestamp': '2018-05-08T16:59:35.746Z',
                'SignatureVersion': '1',
                'Signature': 'Y9AIS71BI3dU5DqeF1AEFm0bSkNAQcgq5CkphEN9psd4cGlMr8AaRinIxhJcdGBLmMMYHWJWgDnvkDhxT0zWF1Q6AVM7H0gNDans48M6q/2frMZ/YQaQDtRWxBRpsO3Y/oi02lj/jbP4odo7Eeye6II8GAt0lbpPLCgqFud0+naYmtNj4qJMY4c19oaRuRIrYlCwZ7UdYWu7zD8orfIYCwLdq1E/i3jpPZ7ZUCLyZj/FoTiI5MnBvDI0O6B0EtTixNvwum07PUdCxPSvWWrtuI6jXW2yruVgt0sLKaGq5OXqqWY8GWW4EN9O3AfQ2XXW1FASLBrfyLDCaiT/FpnqsQ==',
                'SigningCertURL': 'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-eaea6120e66ea12e88dcd8bcbddca752.pem',
                'UnsubscribeURL': 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:01234567890:ecs-lifecycle-hook:42db8ba1-a29f-4dc4-aeda-073284e9971b'
            }
        }
    ]
}

termination_message_json = termination_event['Records'][0]['Sns']

termination_message = {
    'AccountId': '01234567890',
    'AutoScalingGroupName': 'testing-ECSAutoScalingGroup-J80BFBLVR4ZJ',
    'EC2InstanceId': 'i-01234567890abcdef',
    'LifecycleActionToken': 'e0ad7bf9-2746-4322-982f-0b0c9a6eb929',
    'LifecycleHookName': 'testing-ASGTerminateHook-11414UVQ4RWSR',
    'LifecycleTransition': 'autoscaling:EC2_INSTANCE_TERMINATING',
    'RequestId': 'f8218720-3d16-4a5b-b037-74df1318de90',
    'Service': 'AWS Auto Scaling',
    'Time': '2018-05-07T15:31:19.598Z'
}

launch_event = {
    'Records': [
        {
            'EventSource': 'aws:sns',
            'EventSubscriptionArn': 'arn:aws:sns:us-east-1:01234567890:ecs-lifecycle-hook:0ecad48e-b088-42eb-adf5-ff5cf998b276',
            'EventVersion': '1.0',
            'Sns': {
                'Message': '{"AccountId": "01234567890", "AutoScalingGroupName": "testing-ECSAutoScalingGroup-J80BFBLVR4ZJ", "EC2InstanceId": "i-01234567890abcdef", "LifecycleActionToken": "e0ad7bf9-2746-4322-982f-0b0c9a6eb929", "LifecycleHookName": "testing-ASGTerminateHook-11414UVQ4RWSR", "LifecycleTransition": "autoscaling:EC2_INSTANCE_LAUNCHING", "RequestId": "f8218720-3d16-4a5b-b037-74df1318de90", "Service": "AWS Auto Scaling", "Time": "2018-05-07T15:31:19.598Z"}',
                'MessageAttributes': {},
                'MessageId': 'e5f51473-71cd-53a2-ae8a-4719077cd3ea',
                'Signature': 'fywyxnj1l4vMMqNPm8V7pvdAcu9zVsUAhd/Rz48eNWCJhxbaB5a3MziFLPDFnMRlIKPKgTSTwG4W/ElrcMbS9TCMCudB/i4Zr/Ao98dpbx1NpGIDZAeZsupWknBLMHwsCb0MLU4up1VLnYkMeuXPNX2QxyUbwWEeeLsUkc9MI7h1TOG+P+NicifaFmEGHsrP2oGas6TYqx4xrRyBj7mBLBST5oOEBlik2ebyr2qjvXIjR1riT25DQd3OLaHjZ0jPjdIn9rwgJJ5nx0Qa6mAS8olm20ABwAm362/BkPEZ5Q1HJ+1DXoFs9xAqpUvEJKm/5WkfCU7fvNs4mQrSuZZT4g==',
                'SignatureVersion': '1',
                'SigningCertUrl': 'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-eaea6120e66ea12e88dcd8bcbddca752.pem',
                'Subject': 'Auto Scaling: termination',
                'Timestamp': '2018-05-07T15:44:49.382Z',
                'TopicArn': 'arn:aws:sns:us-east-1:01234567890:ecs-lifecycle-hook',
                'Type': 'Notification',
                'UnsubscribeUrl': 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:01234567890:ecs-lifecycle-hook:0ecad48e-b088-42eb-adf5-ff5cf998b276'
            }
        }
    ]
}

launch_message_json = launch_event['Records'][0]['Sns']

launch_message = {
    'AccountId': '01234567890',
    'AutoScalingGroupName': 'testing-ECSAutoScalingGroup-J80BFBLVR4ZJ',
    'EC2InstanceId': 'i-01234567890abcdef',
    'LifecycleActionToken': 'e0ad7bf9-2746-4322-982f-0b0c9a6eb929',
    'LifecycleHookName': 'testing-ASGTerminateHook-11414UVQ4RWSR',
    'LifecycleTransition': 'autoscaling:EC2_INSTANCE_LAUNCHING',
    'RequestId': 'f8218720-3d16-4a5b-b037-74df1318de90',
    'Service': 'AWS Auto Scaling',
    'Time': '2018-05-07T15:31:19.598Z'
}

non_lifecycle_event = {
    'Records': [
        {
            'EventSource': 'aws:sns',
            'EventSubscriptionArn': 'arn:aws:sns:us-east-1:01234567890:ecs-lifecycle-hook:0ecad48e-b088-42eb-adf5-ff5cf998b276',
            'EventVersion': '1.0',
            'Sns': {
                'Message': '{"Progress":60,"AccountId":"01234567890","Description":"Terminating EC2 instance: i-01234567890abcdef","RequestId":"f753f11f-5d66-41f1-bcf6-f2db8aa09930","EndTime":"2018-05-07T15:44:49.318Z","AutoScalingGroupARN":"arn:aws:autoscaling:us-east-1:01234567890:autoScalingGroup:dd62e2fb-d40a-4c9e-8427-eac61d400f0b:autoScalingGroupName/testing-ECSAutoScalingGroup-J80BFBLVR4ZJ","ActivityId":"f753f11f-5d66-41f1-bcf6-f2db8aa09930","StartTime":"2018-05-07T15:14:46.548Z","Service":"AWS Auto Scaling","Time":"2018-05-07T15:44:49.318Z","EC2InstanceId":"i-01234567890abcdef","StatusCode":"MidTerminatingLifecycleAction","StatusMessage":"","Details":{"Subnet ID":"subnet-0ab1c2d3","Availability Zone":"us-east-1a"},"AutoScalingGroupName":"testing-ECSAutoScalingGroup-J80BFBLVR4ZJ","Cause":"At 2018-05-07T15:14:41Z a user request update of AutoScalingGroup constraints to min: 1, max: 3, desired: 2 changing the desired capacity from 3 to 2. At 2018-05-07T15:14:46Z an instance was taken out of service in response to a difference between desired and actual capacity, shrinking the capacity from 3 to 2. At 2018-05-07T15:14:46Z instance i-01234567890abcdef was selected for termination.","Event":"autoscaling:EC2_INSTANCE_TERMINATE"}',
                'MessageAttributes': {},
                'MessageId': 'e5f51473-71cd-53a2-ae8a-4719077cd3ea',
                'Signature': 'fywyxnj1l4vMMqNPm8V7pvdAcu9zVsUAhd/Rz48eNWCJhxbaB5a3MziFLPDFnMRlIKPKgTSTwG4W/ElrcMbS9TCMCudB/i4Zr/Ao98dpbx1NpGIDZAeZsupWknBLMHwsCb0MLU4up1VLnYkMeuXPNX2QxyUbwWEeeLsUkc9MI7h1TOG+P+NicifaFmEGHsrP2oGas6TYqx4xrRyBj7mBLBST5oOEBlik2ebyr2qjvXIjR1riT25DQd3OLaHjZ0jPjdIn9rwgJJ5nx0Qa6mAS8olm20ABwAm362/BkPEZ5Q1HJ+1DXoFs9xAqpUvEJKm/5WkfCU7fvNs4mQrSuZZT4g==',
                'SignatureVersion': '1',
                'SigningCertUrl': 'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-eaea6120e66ea12e88dcd8bcbddca752.pem',
                'Subject': 'Auto Scaling: termination',
                'Timestamp': '2018-05-07T15:44:49.382Z',
                'TopicArn': 'arn:aws:sns:us-east-1:01234567890:ecs-lifecycle-hook',
                'Type': 'Notification',
                'UnsubscribeUrl': 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:01234567890:ecs-lifecycle-hook:0ecad48e-b088-42eb-adf5-ff5cf998b276'
            }
        }
    ]
}

non_lifecycle_message_json = non_lifecycle_event['Records'][0]['Sns']

non_lifecycle_message = {
    'AccountId': '01234567890',
    'ActivityId': 'f753f11f-5d66-41f1-bcf6-f2db8aa09930',
    'AutoScalingGroupARN': 'arn:aws:autoscaling:us-east-1:01234567890:autoScalingGroup:dd62e2fb-d40a-4c9e-8427-eac61d400f0b:autoScalingGroupName/testing-ECSAutoScalingGroup-J80BFBLVR4ZJ',
    'AutoScalingGroupName': 'testing-ECSAutoScalingGroup-J80BFBLVR4ZJ',
    'Cause': 'At 2018-05-07T15:14:41Z a user request update of AutoScalingGroup constraints to min: 1, max: 3, desired: 2 changing the desired capacity from 3 to 2. At 2018-05-07T15:14:46Z an instance was taken out of service in response to a difference between desired and actual capacity, shrinking the capacity from 3 to 2. At 2018-05-07T15:14:46Z instance i-01234567890abcdef was selected for termination.',
    'Description': 'Terminating EC2 instance: i-01234567890abcdef',
    'Details': {
        'Availability Zone': 'us-east-1a',
        'Subnet ID': 'subnet-0ab1c2d3'
    },
    'EC2InstanceId': 'i-01234567890abcdef',
    'EndTime': '2018-05-07T15:44:49.318Z',
    'Event': 'autoscaling:EC2_INSTANCE_TERMINATE',
    'Progress': 60,
    'RequestId': 'f753f11f-5d66-41f1-bcf6-f2db8aa09930',
    'Service': 'AWS Auto Scaling',
    'StartTime': '2018-05-07T15:14:46.548Z',
    'StatusCode': 'MidTerminatingLifecycleAction',
    'StatusMessage': '',
    'Time': '2018-05-07T15:44:49.318Z'
}

container_instance_arn = 'arn:aws:ecs:us-east-1:01234567890:container-instance/11a3d023-f796-449f-8381-7f5f4137ac50'

container_instance_active = {
    'containerInstanceArn': 'arn:aws:ecs:us-east-1:01234567890:container-instance/4336ffad-f3af-41a3-b1f0-e20ba7db2c82',
    'ec2InstanceId': 'i-01234567890abcdef',
    'version': 124,
    'versionInfo': {
        'agentVersion': '1.17.2',
        'agentHash': 'edc3e260',
        'dockerVersion': 'DockerVersion: 17.12.0-ce'
    },
    'remainingResources': [
        {'name': 'CPU',
         'type': 'INTEGER',
         'doubleValue': 0.0,
         'longValue': 0,
         'integerValue': 2026
         },
        {
            'name': 'MEMORY',
            'type': 'INTEGER',
            'doubleValue': 0.0,
            'longValue': 0,
            'integerValue': 6566
        },
        {
            'name': 'PORTS',
            'type': 'STRINGSET',
            'doubleValue': 0.0,
            'longValue': 0,
            'integerValue': 0,
            'stringSetValue': ['22', '2376', '2375', '51678', '51679']
        },
        {
            'name': 'PORTS_UDP',
            'type': 'STRINGSET',
            'doubleValue': 0.0,
            'longValue': 0,
            'integerValue': 0,
            'stringSetValue': []
        }
    ],
    'registeredResources': [
        {
            'name': 'CPU',
            'type': 'INTEGER',
            'doubleValue': 0.0,
            'longValue': 0,
            'integerValue': 2048
        },
        {
            'name': 'MEMORY',
            'type': 'INTEGER',
            'doubleValue': 0.0,
            'longValue': 0,
            'integerValue': 7690
        },
        {
            'name': 'PORTS',
            'type': 'STRINGSET',
            'doubleValue': 0.0,
            'longValue': 0,
            'integerValue': 0,
            'stringSetValue': ['22', '2376', '2375', '51678', '51679']
        },
        {
            'name': 'PORTS_UDP',
            'type': 'STRINGSET',
            'doubleValue': 0.0,
            'longValue': 0,
            'integerValue': 0,
            'stringSetValue': []
        }
    ],
    'status': 'ACTIVE',
    'agentConnected': True,
    'runningTasksCount': 8,
    'pendingTasksCount': 0,
    'attributes': [
        {'name': 'com.amazonaws.ecs.capability.logging-driver.syslog'},
        {'name': 'ecs.ami-id', 'value': 'ami-abcd1234'},
        {'name': 'com.amazonaws.ecs.capability.logging-driver.none'},
        {'name': 'com.amazonaws.ecs.capability.logging-driver.json-file'},
        {'name': 'ecs.vpc-id', 'value': 'vpc-0ab1c2d3'},
        {'name': 'ecs.capability.execution-role-awslogs'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.17'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.18'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.19'},
        {'name': 'ecs.capability.task-cpu-mem-limit'},
        {'name': 'ecs.capability.task-eni'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.30'},
        {'name': 'ecs.capability.execution-role-ecr-pull'},
        {'name': 'ecs.capability.container-health-check'},
        {'name': 'ecs.subnet-id', 'value': 'subnet-0ab1c2d3'},
        {'name': 'ecs.availability-zone', 'value': 'us-east-1b'},
        {'name': 'ecs.instance-type', 'value': 'm5.large'},
        {'name': 'com.amazonaws.ecs.capability.task-iam-role-network-host'},
        {'name': 'com.amazonaws.ecs.capability.logging-driver.awslogs'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.24'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.25'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.26'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.27'},
        {'name': 'com.amazonaws.ecs.capability.privileged-container'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.28'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.29'},
        {'name': 'ecs.capability.cni-plugin-version',
         'value': '0c6216c-2018.02.0'},
        {'name': 'com.amazonaws.ecs.capability.ecr-auth'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.20'},
        {'name': 'ecs.os-type', 'value': 'linux'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.21'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.22'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.23'},
        {'name': 'com.amazonaws.ecs.capability.task-iam-role'}],
    'registeredAt': datetime.datetime(2018, 5, 7, 16, 49, 8, 905000,
                                      tzinfo=tzlocal()),
    'attachments': []
}

container_instance_draining = {
    'containerInstanceArn': 'arn:aws:ecs:us-east-1:01234567890:container-instance/4336ffad-f3af-41a3-b1f0-e20ba7db2c82',
    'ec2InstanceId': 'i-01234567890abcdef',
    'version': 124,
    'versionInfo': {
        'agentVersion': '1.17.2',
        'agentHash': 'edc3e260',
        'dockerVersion': 'DockerVersion: 17.12.0-ce'
    },
    'remainingResources': [
        {'name': 'CPU',
         'type': 'INTEGER',
         'doubleValue': 0.0,
         'longValue': 0,
         'integerValue': 2026
         },
        {
            'name': 'MEMORY',
            'type': 'INTEGER',
            'doubleValue': 0.0,
            'longValue': 0,
            'integerValue': 6566
        },
        {
            'name': 'PORTS',
            'type': 'STRINGSET',
            'doubleValue': 0.0,
            'longValue': 0,
            'integerValue': 0,
            'stringSetValue': ['22', '2376', '2375', '51678', '51679']
        },
        {
            'name': 'PORTS_UDP',
            'type': 'STRINGSET',
            'doubleValue': 0.0,
            'longValue': 0,
            'integerValue': 0,
            'stringSetValue': []
        }
    ],
    'registeredResources': [
        {
            'name': 'CPU',
            'type': 'INTEGER',
            'doubleValue': 0.0,
            'longValue': 0,
            'integerValue': 2048
        },
        {
            'name': 'MEMORY',
            'type': 'INTEGER',
            'doubleValue': 0.0,
            'longValue': 0,
            'integerValue': 7690
        },
        {
            'name': 'PORTS',
            'type': 'STRINGSET',
            'doubleValue': 0.0,
            'longValue': 0,
            'integerValue': 0,
            'stringSetValue': ['22', '2376', '2375', '51678', '51679']
        },
        {
            'name': 'PORTS_UDP',
            'type': 'STRINGSET',
            'doubleValue': 0.0,
            'longValue': 0,
            'integerValue': 0,
            'stringSetValue': []
        }
    ],
    'status': 'DRAINING',
    'agentConnected': True,
    'runningTasksCount': 8,
    'pendingTasksCount': 0,
    'attributes': [
        {'name': 'com.amazonaws.ecs.capability.logging-driver.syslog'},
        {'name': 'ecs.ami-id', 'value': 'ami-abcd1234'},
        {'name': 'com.amazonaws.ecs.capability.logging-driver.none'},
        {'name': 'com.amazonaws.ecs.capability.logging-driver.json-file'},
        {'name': 'ecs.vpc-id', 'value': 'vpc-0ab1c2d3'},
        {'name': 'ecs.capability.execution-role-awslogs'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.17'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.18'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.19'},
        {'name': 'ecs.capability.task-cpu-mem-limit'},
        {'name': 'ecs.capability.task-eni'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.30'},
        {'name': 'ecs.capability.execution-role-ecr-pull'},
        {'name': 'ecs.capability.container-health-check'},
        {'name': 'ecs.subnet-id', 'value': 'subnet-0ab1c2d3'},
        {'name': 'ecs.availability-zone', 'value': 'us-east-1b'},
        {'name': 'ecs.instance-type', 'value': 'm5.large'},
        {'name': 'com.amazonaws.ecs.capability.task-iam-role-network-host'},
        {'name': 'com.amazonaws.ecs.capability.logging-driver.awslogs'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.24'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.25'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.26'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.27'},
        {'name': 'com.amazonaws.ecs.capability.privileged-container'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.28'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.29'},
        {'name': 'ecs.capability.cni-plugin-version',
         'value': '0c6216c-2018.02.0'},
        {'name': 'com.amazonaws.ecs.capability.ecr-auth'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.20'},
        {'name': 'ecs.os-type', 'value': 'linux'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.21'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.22'},
        {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.23'},
        {'name': 'com.amazonaws.ecs.capability.task-iam-role'}],
    'registeredAt': datetime.datetime(2018, 5, 7, 16, 49, 8, 905000,
                                      tzinfo=tzlocal()),
    'attachments': []
}

list_container_instances_response = {
    'containerInstanceArns': [
        'arn:aws:ecs:us-east-1:01234567890:container-instance/4336ffad-f3af-41a3-b1f0-e20ba7db2c82',
        'arn:aws:ecs:us-east-1:01234567890:container-instance/ae9c9e03-2ae2-4ead-8c15-16f501126295',
        'arn:aws:ecs:us-east-1:01234567890:container-instance/c97b2a54-527c-47ed-9296-69a895607c0f'
    ],
    'ResponseMetadata': {
        'RequestId': '91a77486-52e1-11e8-bf48-c92eed6dc417',
        'HTTPStatusCode': 200,
        'HTTPHeaders': {
            'server': 'Server',
            'date': 'Tue, 08 May 2018 17:02:19 GMT',
            'content-type': 'application/x-amz-json-1.1',
            'content-length': '306',
            'connection': 'keep-alive',
            'x-amzn-requestid': '91a77486-52e1-11e8-bf48-c92eed6dc417'},
        'RetryAttempts': 0
    }
}

describe_container_instances_response = {
    'containerInstances': [
        {
            'containerInstanceArn': 'arn:aws:ecs:us-east-1:01234567890:container-instance/4336ffad-f3af-41a3-b1f0-e20ba7db2c82',
            'ec2InstanceId': 'i-01234567890abcdef',
            'version': 124,
            'versionInfo': {
                'agentVersion': '1.17.2',
                'agentHash': 'edc3e260',
                'dockerVersion': 'DockerVersion: 17.12.0-ce'
            },
            'remainingResources': [
                {'name': 'CPU',
                 'type': 'INTEGER',
                 'doubleValue': 0.0,
                 'longValue': 0,
                 'integerValue': 2026
                 },
                {'name': 'MEMORY',
                 'type': 'INTEGER',
                 'doubleValue': 0.0,
                 'longValue': 0,
                 'integerValue': 6566
                 },
                {'name': 'PORTS',
                 'type': 'STRINGSET',
                 'doubleValue': 0.0,
                 'longValue': 0,
                 'integerValue': 0,
                 'stringSetValue': ['22', '2376', '2375', '51678', '51679']
                 },
                {'name': 'PORTS_UDP',
                 'type': 'STRINGSET',
                 'doubleValue': 0.0,
                 'longValue': 0,
                 'integerValue': 0,
                 'stringSetValue': []
                 }
            ],
            'registeredResources': [
                {
                    'name': 'CPU',
                    'type': 'INTEGER',
                    'doubleValue': 0.0,
                    'longValue': 0,
                    'integerValue': 2048
                },
                {
                    'name': 'MEMORY',
                    'type': 'INTEGER',
                    'doubleValue': 0.0,
                    'longValue': 0,
                    'integerValue': 7690
                },
                {
                    'name': 'PORTS',
                    'type': 'STRINGSET',
                    'doubleValue': 0.0,
                    'longValue': 0,
                    'integerValue': 0,
                    'stringSetValue': ['22', '2376', '2375', '51678', '51679']
                },
                {
                    'name': 'PORTS_UDP',
                    'type': 'STRINGSET',
                    'doubleValue': 0.0,
                    'longValue': 0,
                    'integerValue': 0,
                    'stringSetValue': []
                }
            ],
            'status': 'ACTIVE',
            'agentConnected': True,
            'runningTasksCount': 8,
            'pendingTasksCount': 0,
            'attributes': [
                {'name': 'com.amazonaws.ecs.capability.logging-driver.syslog'},
                {'name': 'ecs.ami-id', 'value': 'ami-abcd1234'},
                {'name': 'com.amazonaws.ecs.capability.logging-driver.none'},
                {
                    'name': 'com.amazonaws.ecs.capability.logging-driver.json-file'},
                {'name': 'ecs.vpc-id', 'value': 'vpc-0ab1c2d3'},
                {'name': 'ecs.capability.execution-role-awslogs'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.17'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.18'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.19'},
                {'name': 'ecs.capability.task-cpu-mem-limit'},
                {'name': 'ecs.capability.task-eni'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.30'},
                {'name': 'ecs.capability.execution-role-ecr-pull'},
                {'name': 'ecs.capability.container-health-check'},
                {'name': 'ecs.subnet-id', 'value': 'subnet-0ab1c2d3'},
                {'name': 'ecs.availability-zone', 'value': 'us-east-1b'},
                {'name': 'ecs.instance-type', 'value': 'm5.large'},
                {
                    'name': 'com.amazonaws.ecs.capability.task-iam-role-network-host'},
                {
                    'name': 'com.amazonaws.ecs.capability.logging-driver.awslogs'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.24'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.25'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.26'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.27'},
                {'name': 'com.amazonaws.ecs.capability.privileged-container'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.28'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.29'},
                {'name': 'ecs.capability.cni-plugin-version',
                 'value': '0c6216c-2018.02.0'},
                {'name': 'com.amazonaws.ecs.capability.ecr-auth'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.20'},
                {'name': 'ecs.os-type', 'value': 'linux'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.21'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.22'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.23'},
                {'name': 'com.amazonaws.ecs.capability.task-iam-role'}
            ],
            'registeredAt': datetime.datetime(2018, 5, 7, 16, 49, 8, 905000,
                                              tzinfo=tzlocal()),
            'attachments': []
        },
        {
            'containerInstanceArn': 'arn:aws:ecs:us-east-1:01234567890:container-instance/ae9c9e03-2ae2-4ead-8c15-16f501126295',
            'ec2InstanceId': 'i-01234567890abcdef',
            'version': 123,
            'versionInfo': {
                'agentVersion': '1.17.2',
                'agentHash': 'edc3e260',
                'dockerVersion': 'DockerVersion: 17.12.0-ce'
            },
            'remainingResources': [
                {
                    'name': 'CPU',
                    'type': 'INTEGER',
                    'doubleValue': 0.0,
                    'longValue': 0,
                    'integerValue': 2036
                },
                {
                    'name': 'MEMORY',
                    'type': 'INTEGER',
                    'doubleValue': 0.0,
                    'longValue': 0,
                    'integerValue': 6922
                },
                {
                    'name': 'PORTS',
                    'type': 'STRINGSET',
                    'doubleValue': 0.0,
                    'longValue': 0,
                    'integerValue': 0,
                    'stringSetValue': [
                        '22', '2376', '2375', '51678', '51679']
                },
                {
                    'name': 'PORTS_UDP',
                    'type': 'STRINGSET',
                    'doubleValue': 0.0,
                    'longValue': 0,
                    'integerValue': 0,
                    'stringSetValue': []
                }
            ],
            'registeredResources': [
                {
                    'name': 'CPU',
                    'type': 'INTEGER',
                    'doubleValue': 0.0,
                    'longValue': 0,
                    'integerValue': 2048
                },
                {
                    'name': 'MEMORY',
                    'type': 'INTEGER',
                    'doubleValue': 0.0,
                    'longValue': 0,
                    'integerValue': 7690
                },
                {
                    'name': 'PORTS',
                    'type': 'STRINGSET',
                    'doubleValue': 0.0,
                    'longValue': 0,
                    'integerValue': 0,
                    'stringSetValue': ['22', '2376', '2375', '51678', '51679']
                },
                {
                    'name': 'PORTS_UDP',
                    'type': 'STRINGSET',
                    'doubleValue': 0.0,
                    'longValue': 0,
                    'integerValue': 0,
                    'stringSetValue': []
                }
            ],
            'status': 'DRAINING',
            'agentConnected': True,
            'runningTasksCount': 6,
            'pendingTasksCount': 0,
            'attributes': [
                {'name': 'com.amazonaws.ecs.capability.logging-driver.syslog'},
                {'name': 'ecs.ami-id', 'value': 'ami-abcd1234'},
                {'name': 'com.amazonaws.ecs.capability.logging-driver.none'},
                {
                    'name': 'com.amazonaws.ecs.capability.logging-driver.json-file'},
                {'name': 'ecs.capability.execution-role-awslogs'},
                {'name': 'ecs.vpc-id', 'value': 'vpc-0ab1c2d3'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.17'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.18'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.19'},
                {'name': 'ecs.capability.task-cpu-mem-limit'},
                {'name': 'ecs.capability.task-eni'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.30'},
                {'name': 'ecs.capability.execution-role-ecr-pull'},
                {'name': 'ecs.capability.container-health-check'},
                {'name': 'ecs.subnet-id', 'value': 'subnet-0ab1c2d3'},
                {'name': 'ecs.availability-zone', 'value': 'us-east-1a'},
                {'name': 'ecs.instance-type', 'value': 'm5.large'},
                {
                    'name': 'com.amazonaws.ecs.capability.task-iam-role-network-host'},
                {
                    'name': 'com.amazonaws.ecs.capability.logging-driver.awslogs'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.24'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.25'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.26'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.27'},
                {'name': 'com.amazonaws.ecs.capability.privileged-container'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.28'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.29'},
                {'name': 'ecs.capability.cni-plugin-version',
                 'value': '0c6216c-2018.02.0'},
                {'name': 'com.amazonaws.ecs.capability.ecr-auth'},
                {'name': 'ecs.os-type', 'value': 'linux'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.20'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.21'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.22'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.23'},
                {'name': 'com.amazonaws.ecs.capability.task-iam-role'}
            ],
            'registeredAt': datetime.datetime(2018, 5, 7, 16, 49, 5, 409000,
                                              tzinfo=tzlocal()),
            'attachments': []
        },
        {
            'containerInstanceArn': 'arn:aws:ecs:us-east-1:01234567890:container-instance/c97b2a54-527c-47ed-9296-69a895607c0f',
            'ec2InstanceId': 'i-04de8dd99dcd9d5fd',
            'version': 138,
            'versionInfo': {
                'agentVersion': '1.17.2',
                'agentHash': 'edc3e260',
                'dockerVersion': 'DockerVersion: 17.12.0-ce'
            },
            'remainingResources': [
                {
                    'name': 'CPU',
                    'type': 'INTEGER',
                    'doubleValue': 0.0,
                    'longValue': 0,
                    'integerValue': 2036
                },
                {
                    'name': 'MEMORY',
                    'type': 'INTEGER',
                    'doubleValue': 0.0,
                    'longValue': 0,
                    'integerValue': 6922
                },
                {
                    'name': 'PORTS',
                    'type': 'STRINGSET',
                    'doubleValue': 0.0,
                    'longValue': 0,
                    'integerValue': 0,
                    'stringSetValue': ['22', '2376', '2375',
                                       '51678', '51679']
                },
                {
                    'name': 'PORTS_UDP',
                    'type': 'STRINGSET',
                    'doubleValue': 0.0,
                    'longValue': 0,
                    'integerValue': 0,
                    'stringSetValue': []
                }
            ],
            'registeredResources': [
                {
                    'name': 'CPU',
                    'type': 'INTEGER',
                    'doubleValue': 0.0,
                    'longValue': 0,
                    'integerValue': 2048
                },
                {
                    'name': 'MEMORY',
                    'type': 'INTEGER',
                    'doubleValue': 0.0,
                    'longValue': 0,
                    'integerValue': 7690
                },
                {
                    'name': 'PORTS',
                    'type': 'STRINGSET',
                    'doubleValue': 0.0,
                    'longValue': 0,
                    'integerValue': 0,
                    'stringSetValue': ['22', '2376', '2375', '51678', '51679']
                },
                {
                    'name': 'PORTS_UDP',
                    'type': 'STRINGSET',
                    'doubleValue': 0.0,
                    'longValue': 0,
                    'integerValue': 0,
                    'stringSetValue': []
                }
            ],
            'status': 'DRAINING',
            'agentConnected': True,
            'runningTasksCount': 6,
            'pendingTasksCount': 0,
            'attributes': [
                {'name': 'com.amazonaws.ecs.capability.logging-driver.syslog'},
                {'name': 'ecs.ami-id', 'value': 'ami-abcd1234'},
                {'name': 'com.amazonaws.ecs.capability.logging-driver.none'},
                {
                    'name': 'com.amazonaws.ecs.capability.logging-driver.json-file'},
                {'name': 'ecs.vpc-id', 'value': 'vpc-0ab1c2d3'},
                {'name': 'ecs.capability.execution-role-awslogs'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.17'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.18'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.19'},
                {'name': 'ecs.capability.task-eni'},
                {'name': 'ecs.capability.task-cpu-mem-limit'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.30'},
                {'name': 'ecs.capability.execution-role-ecr-pull'},
                {'name': 'ecs.capability.container-health-check'},
                {'name': 'ecs.subnet-id', 'value': 'subnet-0ab1c2d3'},
                {'name': 'ecs.availability-zone', 'value': 'us-east-1a'},
                {'name': 'ecs.instance-type', 'value': 'm5.large'},
                {
                    'name': 'com.amazonaws.ecs.capability.task-iam-role-network-host'},
                {
                    'name': 'com.amazonaws.ecs.capability.logging-driver.awslogs'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.24'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.25'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.26'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.27'},
                {'name': 'com.amazonaws.ecs.capability.privileged-container'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.28'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.29'},
                {'name': 'ecs.capability.cni-plugin-version',
                 'value': '0c6216c-2018.02.0'},
                {'name': 'com.amazonaws.ecs.capability.ecr-auth'},
                {'name': 'ecs.os-type', 'value': 'linux'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.20'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.21'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.22'},
                {'name': 'com.amazonaws.ecs.capability.task-iam-role'},
                {
                    'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.23'}
            ],
            'registeredAt': datetime.datetime(2018, 5, 7, 15, 17, 16, 181000,
                                              tzinfo=tzlocal()),
            'attachments': []
        }
    ],
    'failures': [],
    'ResponseMetadata': {
        'RequestId': '91b46cda-52e1-11e8-bf48-c92eed6dc417',
        'HTTPStatusCode': 200,
        'HTTPHeaders': {
            'server': 'Server',
            'date': 'Tue, 08 May 2018 17:02:20 GMT',
            'content-type': 'application/x-amz-json-1.1',
            'content-length': '9810',
            'connection': 'keep-alive',
            'x-amzn-requestid': '91b46cda-52e1-11e8-bf48-c92eed6dc417'
        },
        'RetryAttempts': 0
    }
}

list_tasks_response = {
    'taskArns': [
        'arn:aws:ecs:us-east-1:01234567890:task/1c2f3979-4079-4576-84e0-f03e2925e817',
        'arn:aws:ecs:us-east-1:01234567890:task/1f12f433-c34e-4e2f-8d80-97fe61224ca0',
        'arn:aws:ecs:us-east-1:01234567890:task/54445eee-d820-4911-9f96-c2e6d9cca2f6',
        'arn:aws:ecs:us-east-1:01234567890:task/bd8551c2-3f9e-4632-b87e-ac2bb5eeb186',
        'arn:aws:ecs:us-east-1:01234567890:task/e78ee8d1-bb4c-4fe7-a7a9-f9bea2069e90',
        'arn:aws:ecs:us-east-1:01234567890:task/eefa6b92-6c87-43ae-8abf-4ede87a4c631'],
    'ResponseMetadata': {
        'RequestId': 'c20be9cd-52e1-11e8-9a7f-17dd9645a3be',
        'HTTPStatusCode': 200,
        'HTTPHeaders': {
            'server': 'Server',
            'date': 'Tue, 08 May 2018 17:03:41 GMT',
            'content-type': 'application/x-amz-json-1.1',
            'content-length': '488',
            'connection': 'keep-alive',
            'x-amzn-requestid': 'c20be9cd-52e1-11e8-9a7f-17dd9645a3be'
        },
        'RetryAttempts': 0
    }
}

describe_tasks_response = {
    'tasks': [
        {
            'startedBy': '4336ffad-f3af-41a3-b1f0-e20ba7db2c82',
            'taskArn': 'this is a fake task ARN',
            'group': 'family:foobar',
        },
    ]
}

describe_tasks_response_only_daemon_tasks = {
    'tasks': [
        {
            'startedBy': '4336ffad-f3af-41a3-b1f0-e20ba7db2c82',
            'taskArn': 'this is a fake task ARN',
            'group': 'family:foobar',
        },
        {
            'startedBy': '4336ffad-f3af-41a3-b1f0-e20ba7db2c82',
            'taskArn': 'this is a fake task ARN',
            'group': 'family:foobar',
        },
        {
            'startedBy': '4336ffad-f3af-41a3-b1f0-e20ba7db2c82',
            'taskArn': 'this is a fake task ARN',
            'group': 'family:foobar',
        },
    ]
}

describe_tasks_response_mixed_startedby = {
    'tasks': [
        {
            'startedBy': '4336ffad-f3af-41a3-b1f0-e20ba7db2c82',
            'taskArn': 'this is a fake task ARN',
            'group': 'family:foobar',
        },
        {
            'startedBy': 'someone else',
            'taskArn': 'this is a fake task ARN',
            'group': 'family:foobar',
        },
        {
            'startedBy': 'someone else',
            'taskArn': 'this is a fake task ARN',
            'group': 'family:foobar',
        },
    ]
}

describe_tasks_response_only_scheduled_tasks = {
    'tasks': [
        {
            'startedBy': '4336ffad-f3af-41a3-b1f0-e20ba7db2c82',
            'taskArn': 'this is a fake task ARN',
            'group': 'family:foobar',
        },
        {
            'startedBy': 'someone else',
            'taskArn': 'this is a fake task ARN',
            'group': 'family:foobar',
        },
        {
            'startedBy': 'someone else',
            'taskArn': 'this is a fake task ARN',
            'group': 'family:foobar',
        },
    ]
}

describe_tasks_response_no_tasks = {
    'tasks': []
}
