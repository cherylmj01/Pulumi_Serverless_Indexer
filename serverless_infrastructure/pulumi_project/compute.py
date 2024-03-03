import json
import pulumi_aws as aws

def define_lambda_role(bucket_arn, dynamo_db_arn):
    # Define the IAM role for Lambda
    lambda_role = aws.iam.Role("lambdaRole",
        assume_role_policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [{
                "Action":"sts:AssumeRole",
                "Principal":{
                    "Service": "lambda.amazonaws.com",
                },
                "Effect":"Allow",
                "Sid":"",
            }]
        })
    )

    # Policy allowing access to the specific S3 bucket
    s3_policy = aws.iam.Policy("s3Policy",
        policy = bucket_arn.apply(lambda arn:json.dumps({
            "Version": "2012-10-17",
            "Statement":[{
                "Action": ["s3:GetObject"],
                "Resource": [f"{arn}/*"],
                "Effect": "Allow",
            }]
        }))
    )

    # Attach the S3 policy to the Lambda role
    aws.iam.RolePolicyAttachment("s3PolicyAttachment",
        role=lambda_role.name,
        policy_arn=s3_policy.arn
    )

    # Policy allowing access to the specific DynamoDB table
    dynamodb_policy = aws.iam.Policy("dynamodbPolicy",
        policy=dynamo_db_arn.apply(lambda arn:json.dumps({
            "Version":"2012-10-17",
            "Statement":[{
                "Action": ["dynamodb:PutItem", "dynamodb:GetItem"],
                "Resource": [arn],
                "Effect": "Allow",
            }]
        }))                               
    )

    # Attach the dynamodb_policy policy to the Lambda role
    aws.iam.RolePolicyAttachment("dynamodbPolicyAttachment",
        role=lambda_role.name,
        policy_arn=dynamodb_policy.arn
    )

    return lambda_role

    
