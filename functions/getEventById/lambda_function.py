import json
import boto3

dynamodb = boto3.resource('dynamodb')
events_table = dynamodb.Table('EventsTable')

def lambda_handler(event, context):
    try:
        event_id = event['pathParameters']['eventId']
        response = events_table.get_item(Key={'eventId': event_id})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'message': 'Event not found'})
            }
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response['Item'])
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Internal server error'})
        }