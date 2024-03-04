import pulumi
from pulumi import ComponentResource, Output
from pulumi.output import Inputs
import pulumi_aws as aws


class ServerlessInfrastructure(ComponentResource):
    def __init__(self, name: str, opts: pulumi.ResourceOptions = None):
        super().__init__('custom:resource:ServerlessInfrastructure', name, {}, opts)


        # Create an S3 bucket as part of this component
        # Set this component as the parent
        self.bucket = aws.s3.Bucket(f"{name}-bucket",
            bucket = f"{name}-fileindexer-2024",
            opts=pulumi.ResourceOptions(parent=self)
        )
        
         # Create a DynamoDB table as part of this component
        self.index_db = aws.dynamodb.Table(f"{name}-index-table",
            attributes=[aws.dynamodb.TableAttributeArgs(name='id', type='S')],
            hash_key="id",
            billing_mode='PAY_PER_REQUEST',
            opts=pulumi.ResourceOptions(parent=self)
        )
        
        

        # Register output properties for the component
        self.bucket_id = self.bucket.id
        self.table_name = self.index_db.name
        self.table_arn = self.index_db.arn

        self.register_outputs({
            'bucket_id': self.bucket_id,
            'table_name': self.table_name,
            'table_arn': self.table_arn,
        })
        

        

