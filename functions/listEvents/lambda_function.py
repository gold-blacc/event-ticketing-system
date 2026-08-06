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
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('EventsTable')
    
    # Extract path parameters from API Gateway
    path_params = event.get('pathParameters') or {}
    event_id = path_params.get('id')
    
    response = table.get_item(Key={'eventId': event_id})
    item = response.get('Item')
    
    if not item:
        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Event not found"})
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(item, cls=DecimalEncoder)
    }