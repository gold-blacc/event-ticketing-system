import json
import boto3
import uuid
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    events_table = dynamodb.Table('EventsTable')
    registrations_table = dynamodb.Table('RegistrationsTable')

    try:
        body = json.loads(event.get('body', '{}')) if isinstance(event.get('body'), str) else (event.get('body') or {})
    except Exception:
        body = {}

    event_id = body.get('eventId')
    user_name = body.get('userName') or body.get('name')

    if not event_id or not user_name:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Missing required fields: eventId and userName"})
        }

    event_response = events_table.get_item(Key={'eventId': event_id})
    event_item = event_response.get('Item')

    if not event_item:
        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Event not found"})
        }

    capacity = event_item.get('capacity', 0)
    registered = event_item.get('registered', 0)

    if registered >= capacity:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Event is fully booked"})
        }

    registration_id = f"reg-{uuid.uuid4().hex[:8]}"
    registration_item = {
        'registrationId': registration_id,
        'eventId': event_id,
        'userName': user_name,
        'status': 'CONFIRMED'
    }
    registrations_table.put_item(Item=registration_item)

    events_table.update_item(
        Key={'eventId': event_id},
        UpdateExpression="SET registered = registered + :val",
        ExpressionAttributeValues={':val': 1}
    )

    return {
        "statusCode": 201,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "message": "Registration successful",
            "registration": registration_item
        }, cls=DecimalEncoder)
    }