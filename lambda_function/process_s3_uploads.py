import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table_name = 'my-serverless-infra-index-table-a24e71b'

def lambda_handler(event, context):
    table = dynamodb.Table(table_name)
    for record in event['Records']:
        s3_object_key = record['s3']['object']['key']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
