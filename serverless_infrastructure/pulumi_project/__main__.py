"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws
from storage import bucket 
from database import index_db
from compute import define_lambda_role


lambda_role = define_lambda_role(bucket.arn, index_db.arn)
# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)
# Export the table name
pulumi.export('table_name', index_db.name)
# Export the table ARN
pulumi.export('table_arn', index_db.arn)

