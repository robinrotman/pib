import boto3
import json

dynamodb = boto3.resource('dynamodb')
game_table = dynamodb.Table('Games')
leader_table = dynamodb.Table('Leaders')
    
def update_score(game_id, player1_score, player2_score):
    game_table.update_item(
        Key={ 'game_id': game_id },
        UpdateExpression='SET player1_score=:player1_score, player2_score=:player2_score',
        ExpressionAttributeValues={
            ':player1_score': player1_score,
            ':player2_score': player2_score
        }
    )
    
def updateLeaderboard(winner, loser):
    if(leader_exists(winner)):
        add_win(winner)
    else:
        add_leader_with_win(winner)
    if(leader_exists(loser)):
        add_loss(loser)
    else:
        add_leader_with_loss(loser)

def leader_exists(player):
    return 'Item' in leader_table.get_item(Key={ 'email': player })
    
def add_win(player):
    leader_table.update_item(
        Key={ 'email': player },
        UpdateExpression='SET wins = wins + :incr',
        ExpressionAttributeValues={
            ':incr': 1
        }
    )
    
def add_loss(player):
    leader_table.update_item(
        Key={ 'email': player},
        UpdateExpression='SET losses = losses + :incr',
        ExpressionAttributeValues={
            ':incr': 1
        }
    )
    
def add_leader_with_win(player):
    leader_table.put_item(
        Item={
            'email': player,
            'wins': 1,
            'losses': 0
        }
    )
    
def add_leader_with_loss(player):
    leader_table.put_item(
        Item={
            'email': player,
            'wins': 0,
            'losses': 1
        }
    )

def lambda_handler(event, context):
    body = json.loads(event['body'])
    game_id = int(event['pathParameters']['game_id'])
    player1_score = int(body['player1_score'])
    player2_score = int(body['player2_score'])
    game = game_table.get_item(Key={ 'game_id': game_id })['Item']
    winner = game['player1'] if (player1_score > player2_score) else game['player2']
    loser = game['player1'] if (player1_score < player2_score) else game['player2']
    update_score(game_id, player1_score, player2_score)
    updateLeaderboard(winner, loser)
    response = {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'message': 'success!'})
    }
    return response
