"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws


bucket_name = "fileindexer-2023"
bucket = aws.s3.Bucket('my-bucket', bucket=bucket_name)


