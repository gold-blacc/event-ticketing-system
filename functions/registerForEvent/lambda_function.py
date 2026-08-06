import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
events_table = dynamodb.Table('EventsTable')
registrations_table = dynamodb.Table('RegistrationsTable')
sns = boto3.client('sns')
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:340577260283:EventRegistrationNotifications'

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        event_id = body['eventId']
        email = body['email']

        response = events_table.get_item(Key={'eventId': event_id})
        if 'Item' not in response:
            return response_json(404, {'message': 'Event not found'})

        event_item = response['Item']
        if event_item['registered'] >= event_item['capacity']:
            return response_json(400, {'message': 'Event is full'})

        registration_id = str(uuid.uuid4())
        registrations_table.put_item(Item={
            'registrationId': registration_id,
            'eventId': event_id,
            'email': email,
            'registeredAt': datetime.utcnow().isoformat()
        })

        events_table.update_item(
            Key={'eventId': event_id},
            UpdateExpression='SET registered = registered + :inc',
            ExpressionAttributeValues={':inc': 1}
        )

        try:
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=f"You're registered for {event_item['eventName']}!",
                Subject='Event Registration Confirmation'
            )
        except Exception as sns_error:
            print(f"SNS notification failed (non-critical): {sns_error}")

        return response_json(200, {
            'message': 'Registration successful',
            'registrationId': registration_id
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        return response_json(500, {'message': 'Internal server error'})

def response_json(status_code, body_dict):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body_dict)
    }