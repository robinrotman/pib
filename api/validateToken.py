import boto3
import random
import json

dynamodb = boto3.resource('dynamodb')
token_table = dynamodb.Table('Tokens')

def token_exists(token):
    return 'Item' in token_table.get_item(Key={ 'token': token })

def lambda_handler(event, context):
    token = int(event['pathParameters']['token'])
    if (token_exists(token)):
        game_id = int(token_table.get_item(Key={ 'token': token })['Item']['game_id'])
        response = {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'game_id': game_id})
        }
    else:
        response = {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'invalid token'})
        }
    return response
