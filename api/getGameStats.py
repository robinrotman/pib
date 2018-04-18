import boto3
import json

dynamodb = boto3.resource('dynamodb')
game_table = dynamodb.Table('Games')

def game_exists(game_id):
    return 'Item' in game_table.get_item(Key={ 'game_id': game_id })

def lambda_handler(event, context):
    game_id = int(event['pathParameters']['game_id'])
    if (game_exists(game_id)):
        game = game_table.get_item(Key={ 'game_id': game_id })['Item']
        response = {
            "statusCode": 200,
            "headers": {'Access-Control-Allow-Origin': '*'},
            "body": json.dumps({'game_id': int(game['game_id']), 'play_to_score': int(game['play_to_score'])})
        }
    else:
        response = {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'error!'})
        }
    return response
