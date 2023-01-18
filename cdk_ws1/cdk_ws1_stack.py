from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_ecr as ecr,
)


class CdkWs1Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(
            self,
            "CdkWs1Queue",
            visibility_timeout=Duration.seconds(300),
        )

        topic = sns.Topic(self, "CdkWs1Topic")

        topic.add_subscription(subs.SqsSubscription(queue))

        ### our stacks
        # L1

        cfn_repository = ecr.CfnRepository(
            self,
            "RepoL1",
            # encryption_configuration=ecr.CfnRepository.EncryptionConfigurationProperty(
            #    encryption_type="kms",
            #    kms_key="kmsKey",
            # ),
            image_scanning_configuration=ecr.CfnRepository.ImageScanningConfigurationProperty(
                scan_on_push=False
            ),
            # lifecycle_policy=ecr.CfnRepository.LifecyclePolicyProperty(
            #    lifecycle_policy_text="lifecyclePolicyText", registry_id="registryId"
            # ),
            repository_name="repo-l1",
        )
        # L2
        repository = ecr.Repository(self, "repo-l2")

        # L2 iam examples
        self.role_policy = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    actions=["ec2:StartInstances", "ec2:StopInstances"],
                    effect=iam.Effect.ALLOW,
                    resources=["*"],
                )
            ]
        )

        self.kms_policy_document = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    actions=["kms:*"],
                    effect=iam.Effect.ALLOW,
                    resources=["*"],
                )
            ]
        )

        self.job_role = iam.Role(
            self,
            id="ecs-job-role",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            role_name=f"ecs-job-role",
            description="Allows ECS tasks to call AWS services on your behalf",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonRDSFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "SecretsManagerReadWrite"
                ),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "CloudWatchLogsFullAccess"
                ),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AmazonECSTaskExecutionRolePolicy"
                ),
            ],
            inline_policies={
                "KMSPolicyDocument": self.kms_policy_document,
                "RolePolicyDocument": self.role_policy,
            },
        )
