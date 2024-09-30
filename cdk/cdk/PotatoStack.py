from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3,
    aws_ses as ses,
    aws_iam as iam,
    aws_bedrock as bedrock
)
from constructs import Construct

import aws_cdk as cdk

class PotatoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "CdkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        bucket = s3.Bucket(self, 
                           "cgiar-files-v2", # Change bucket name to your preference
                           versioned=False
                          )
        
        bedrock.FoundationModel.from_foundation_model_id(self, "anthropic.claude-3-sonnet-20240229-v1:0", bedrock.FoundationModelIdentifier.ANTHROPIC_CLAUDE_3_SONNET_20240229_V1_0)
        my_param = self.node.try_get_context('ses_email')
        # my_param = cdk.CfnParameter(self, "email_param", type="String", description="Email ID for ses")

        ses.EmailIdentity(self, 'Identity', identity= ses.Identity.email(my_param)) # Change this email depending on who need access

        # SES service for sending emails
        # ses_role = iam.Role(self, 
        #                     "SESRole",
        #                     assumed_by=iam.ServicePrincipal("ses.amazonaws.com")
        #                    )
        
        # ses_policy = iam.PolicyStatement(
        #     effect=iam.Effect.ALLOW,
        #     actions=["ses:SendEmail", "ses:SendRawEmail"],
        #     resources=["*"]
        # )
        # ses_role.add_to_policy(ses_policy)

        # # Amazon Bedrock integration
        # bedrock_role = iam.Role(self, 
        #                         "BedrockRole",
        #                         assumed_by=iam.ServicePrincipal("bedrock.amazonaws.com")  # Placeholder
        #                        )
        
        # bedrock_policy = iam.PolicyStatement(
        #     effect=iam.Effect.ALLOW,
        #     actions=["bedrock:InvokeModel", "bedrock:ListModels"],
        #     resources=["*"]  # Adjust resources as per your models
        # )
        
        # bedrock_role.add_to_policy(bedrock_policy)

        # Outputs
        cdk.CfnOutput(self, "BucketName", value=bucket.bucket_name)