import pulumi
import pulumi_aws as aws
from serverless_component import ServerlessInfrastructure
from compute import define_lambda_role

# Instantiate the serverless infrastructure component
serverless_infra = ServerlessInfrastructure('my-serverless-infra')

lambda_role = define_lambda_role(serverless_infra.bucket.arn, serverless_infra.index_db.arn)

lambda_function = aws.lambda_.Function("myLambdaFunction",
    code=pulumi.FileArchive("C:\\Users\\13233\\Documents\\Projects\\Pulumi_Serverless_Indexer\\lambda_function\\process_s3_uploads.zip"),
    handler="process_s3_uploads.lambda_handler",
    role=lambda_role.arn,
    runtime="python3.8",
)

# Add permission for S3 to invoke the Lambda function
lambda_invoke_permission = aws.lambda_.Permission("s3InvokePermission",
    action="lambda:InvokeFunction",
    function=lambda_function.name,
    principal="s3.amazonaws.com",
    source_arn=serverless_infra.bucket.arn,
    opts=pulumi.ResourceOptions(depends_on=[lambda_function])
)

# S3 Bucket Notification for Lambda Trigger
bucket_notification = aws.s3.BucketNotification('my-bucket-notification',
    bucket=serverless_infra.bucket.id,
    lambda_functions=[
        aws.s3.BucketNotificationLambdaFunctionArgs(
            lambda_function_arn=lambda_function.arn,
            events=["s3:ObjectCreated:*"],
        ),
    ],
    opts=pulumi.ResourceOptions(depends_on=[lambda_function, lambda_invoke_permission])
)

# Export the name of the bucket
pulumi.export('bucket_name', serverless_infra.bucket.id)
# Export the table name
pulumi.export('table_name', serverless_infra.index_db.name)
# Export the table ARN
pulumi.export('table_arn', serverless_infra.index_db.arn)