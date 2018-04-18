import boto3
import random
import json

dynamodb = boto3.resource('dynamodb')
game_table = dynamodb.Table('Games')
token_table = dynamodb.Table('Tokens')

def token_exists(token):
    return 'Item' in token_table.get_item(Key={ 'token': token })

def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    token = int(body['token'])
    player1 = body['player1']
    player2 = body['player2']
    play_to_score = int(body['play_to_score'])
    if (token_exists(token)):
        game_id = token_table.get_item(Key={ 'token': token })['Item']['game_id']
        game_table.put_item(
            Item={
                'game_id': game_id,
                'player1': player1,
                'player2': player2,
                'play_to_score': play_to_score
            }
        )
        response = {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'success!'})
        }
    else:
        response = {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'error!'})
        }
    return response
