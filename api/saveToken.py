import boto3
import random
import json

dynamodb = boto3.resource('dynamodb')
token_table = dynamodb.Table('Tokens')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    token = int(body['token'])
    game_id = random.randint(0, 100000000)
    token_table.put_item(
        Item={
            'token': token,
            'game_id': game_id
        }
    )
    response = {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'game_id': game_id})
    }
    return response
