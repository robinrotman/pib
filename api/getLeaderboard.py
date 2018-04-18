import boto3
import random
import json

dynamodb = boto3.resource('dynamodb')
leader_table = dynamodb.Table('Leaders')

def format_leader(leader):
    leader['wins'] = int(leader['wins'])
    leader['losses'] = int(leader['losses'])

def lambda_handler(event, context):
    leaders = leader_table.scan()['Items']
    leaders.sort(key=lambda leader: leader['wins'], reverse=True)
    formatted_leaders = list(map(format_leader, leaders))
    response = {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(leaders)
    }
    return response
