import json
import boto3
from decimal import Decimal

# Custom helper to serialize DynamoDB Decimal types
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('EventsTable') # Make sure table name matches yours
    
    response = table.scan()
    items = response.get('Items', [])

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(items, cls=DecimalEncoder) # Pass DecimalEncoder here
    }