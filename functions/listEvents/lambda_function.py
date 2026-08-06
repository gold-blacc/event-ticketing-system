import json
import boto3

dynamodb = boto3.resource('dynamodb')
events_table = dynamodb.Table('EventsTable')

def lambda_handler(event, context):
    try:
        response = events_table.scan()
        events = response.get('Items', [])
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(events)
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Internal server error'})
        }