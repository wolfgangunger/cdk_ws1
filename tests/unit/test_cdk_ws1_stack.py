import aws_cdk as core
import aws_cdk.assertions as assertions
from cdk_ws1.cdk_ws1_stack import CdkWs1Stack


def test_sqs_queue_created():
    app = core.App()
    stack = CdkWs1Stack(app, "cdk-ws1")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::SQS::Queue", {
        "VisibilityTimeout": 300
    })


def test_sns_topic_created():
    app = core.App()
    stack = CdkWs1Stack(app, "cdk-ws1")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::SNS::Topic", 1)
