"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

# Create a DynamoDB table
index_db = aws.dynamodb.Table("index_table", 
    attributes=[
        aws.dynamodb.TableAttributeArgs(
            name='id',
            type='S',
        ),
    ],
    hash_key= "id",
    billing_mode='PAY_PER_REQUEST'
);

