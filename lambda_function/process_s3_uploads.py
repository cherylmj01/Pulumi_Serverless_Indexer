import json
import boto3
from datetime import datetime

# Initialize a Boto3 client for DynamoDB
dynamodb = boto3.resource('dynamodb')

# Specify DynamoDB table name
table_name = 'index_table'

def lambda_handler(event, context):
    # Get the DynamoDB table resource
    table = dynamodb.Table(table_name)

    for record in event['Records']:
        # Get the S3 object key
        s3_object_key = record['s3']['object']['key']

        #Get the current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Write the object key and timestamp to the DynamoDB table
        try:
            response = table.put_item(
                Item = {
                    'id': s3_object_key,
                    'timestamp': timestamp,
                }
            )
            print(f"DynamoDB Response: {json.dumps(response)}")
        except Exception as e:
            print(f"Error writing to DynamoDB: {str(e)}")

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
