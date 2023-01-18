#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_ws1.cdk_ws1_stack import CdkWs1Stack
from vpc.cdk_vpc_stack import CdkVpcStack
from ecs.ecs_cluster import ECSCluster
from ecs.ecs_service import ECSService

app = cdk.App()
stack1 = CdkWs1Stack(app, "cdk-ws1")

vpc_stack = CdkVpcStack(app, "VPC-Stack")
cluster_stack = ECSCluster(app, "ECS-Stack", vpc=vpc_stack.vpc)
service_stack = ECSService(
    app, "ECS-Service", vpc=vpc_stack.vpc, cluster=cluster_stack.cluster
)

app.synth()
