# ecs-lifecycle-hook

This is run as a Lambda function agaist ECS clusters backed by ASGs.  It was inspired by the AWS blog post *[How to Automate Container Instance Draining in Amazon ECS](https://aws.amazon.com/blogs/compute/how-to-automate-container-instance-draining-in-amazon-ecs/)*.

Whenever a lifecycle-enabled ASG terminates a node (for example, scale-in), the terminating instance is placed into a `wait` state and a notification is sent on a configured SNS topic.  This allows this lambda–which is triggered on SNS notifications–to read this event and perform a few steps.

First, if the instance is a member of an ECS cluster, the node is set to `draining`.  Within the limits of the `deploymentConfiguration` in the [service definition](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service_definition_parameters.html), new tasks are launched on `active` nodes. On `draining` nodes, tasks will eventually stop. This process can take some time for services associated with load balancers.

Once the tasks on the `draining` node have been stopped (or until the ASG lifecycle timeout occurs), an API call to the autoscaling group is sent to proceed in terminating the instance. 

This lambda function accomplishes this process with the following process:

1. The SNS notfication for a given instance is checked for ECS cluster membership
1. The node is set to drain
1. Check for *daemon tasks* (which are tasks started by the instance–perhaps at boot–and not by a service)
    a. If only daemon tasks remain, they are stopped
    b. If there are tasks started by services remaining, daemon tasks are **not** stopped
1. Verify that all tasks have been stopped on a given instance
    a. If tasks remain, the notification is re-published to the SNS topic to be re-checked in the future, and the process starts over
1. Notify the autoscaling group to proceed with terminating the instance

## Building

Requires:

* Python 3.6
* `pipenv`

This will build a zip that can be uploaded to S3.  From the project root:

```bash
pip install -r <(pipenv lock -r) -t dist/
cp -a src/*.py dist/
cd dist && zip -r bundle.zip .
aws s3 cp bundle.zip s3://<your-bucket>/bundle.zip
```

## Deploying

See the provided CloudFormation stack file: `stack.yaml`.

## Development

### Installing Dependencies

After you have `pipenv` installed:

```bash
pipenv sync --dev
```

### Tests

The following are required to pass for a successful build:

* `flake8 src/`
* `flake8 --ignore=E501 tests/`
* `PYTHONPATH=src/ pytest --verbose -s`
