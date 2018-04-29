from gpiozero import Button
import json
import os
import time
import random
import requests
from Scoreboard import Scoreboard

API_BASE_URL = os.environ.get('API_BASE_URL')
POST_TOKEN_URL = API_BASE_URL + '/token/'
GAME_URL_TEMPLATE = API_BASE_URL + '/game/{}'
# POST_TOKEN_URL = 'https://1bj8u6759k.execute-api.us-east-2.amazonaws.com/production/token/'
# GET_GAME_URL_BASE = 'https://1bj8u6759k.execute-api.us-east-2.amazonaws.com/production/game/'
# POST_GAME_SCORE_URL_BASE = 'https://1bj8u6759k.execute-api.us-east-2.amazonaws.com/production/game/'

BUTTON1_GPIO = 5
BUTTON2_GPIO = 6
BUTTON3_GPIO = 12
BUTTON_HOLD_TIME = 3
SLEEP_TIMEOUT = 15 * 60

SLEEP_STATE = 'sleep'
SETUP_STATE = 'setup'
ONLINE_SETUP_STATE = 'online_setup'
GAME_STATE = 'game'
GAME_OVER_STATE = 'game_over'

button1 = Button(BUTTON1_GPIO)
button2 = Button(BUTTON2_GPIO)
button3 = Button(BUTTON3_GPIO)

button1.hold_time = BUTTON_HOLD_TIME
button2.hold_time = BUTTON_HOLD_TIME
button3.hold_time = BUTTON_HOLD_TIME

scoreboard = Scoreboard('yellow', 'blue')
time_of_last_interaction = time.time()
game_id = None
state = SLEEP_STATE
play_to_score = 25
scores = [0, 0]

#States
def setup_online():
    print("ONLINE SETUP")
    reset_buttons()
    state = ONLINE_SETUP_STATE
    button1.when_held = play_game_if_both_pressed
    token = generate_token()
    print("TOKEN = %s" % (token))
    game_id = write_token_to_aws(token)
    scoreboard.show_token(token)
    while not has_reached_timeout():
        req = requests.get(GAME_URL_TEMPLATE.format(game_id))
        if(req.status_code == 200):
            res = req.json()
            play_to_score = int(res['play_to_score'])
            break
        else:
            time.sleep(1)
    if (has_reached_timeout()):
        sleep()
    else:
        play_game()

def play_game():
    print("GAME START")
    reset_buttons()
    state = GAME_STATE
    scoreboard.show_score(scores[0], scores[1])
    button1.when_pressed = increase_player1_score
    button1.when_held = decrease_player1_score
    button3.when_pressed = increase_player2_score
    button3.when_held = decrease_player2_score
    button2.when_held = setup_online

def game_over():
    print("GAME OVER")
    reset_buttons()
    state = GAME_OVER_STATE
    button2.when_held = setup_online
    scoreboard.show_final_score(scores[0], scores[1])
    if game_id:
        print('write to aws')
        payload = { 'game_id': game_id, 'player1_score': scores[0], 'player2_score': scores[1]}
        req = requests.post(GAME_URL_TEMPLATE.format(game_id), json=payload)

def sleep():
    print("GOING TO SLEEP")
    reset_buttons()
    reset()
    state = SLEEP_STATE
    button1.when_held = play_game_if_both_pressed
    button2.when_held = setup_online

#Button Functions
def increase_score(player_index):
    print("INCREASING PLAYER%d score" % (player_index))
    time_of_last_interaction = time.time()
    scores[player_index] += 1
    scoreboard.show_score(scores[0], scores[1])

def decrease_score(player_index):
    print("DECREASING PLAYER%d score" % (player_index))
    time_of_last_interaction = time.time()
    scores[player_index] -= 2
    scoreboard.show_score(scores[0], scores[1])

def increase_player1_score():
    time_of_last_interaction = time.time()
    increase_score(0)

def increase_player2_score():
    time_of_last_interaction = time.time()
    increase_score(1)

def decrease_player1_score():
    time_of_last_interaction = time.time()
    decrease_score(0)

def decrease_player2_score():
    time_of_last_interaction = time.time()
    decrease_score(1)

def play_game_if_both_pressed():
    if(button1.is_pressed() and button3.is_pressed()):
        print("QUICK START")
        play_game()

def reset_buttons():
    print("RESETTING BUTTONS")
    button1.when_pressed = None
    button2.when_pressed = None
    button3.when_pressed = None
    button1.when_held = None
    button2.when_held = None
    button3.when_held = None

#Helpers
def reset():
    print("RESET")
    time_of_last_interaction = time.time()
    game_id = None
    play_to_score = 25
    scores = [0, 0]

def generate_token():
    print("GENERATING TOKEN")
    return random.randint(1000, 10000)

def is_game_over():
    print("CHECKING IS GAME OVER")
    return (((max(scores) >= play_to_score) and has_won_by_two()) or max(scores) == 99)

def has_won_by_two():
    return abs(scores[0] - scores[1]) >= 2

def has_reached_timeout():
    return time.time() - time_of_last_interaction >= SLEEP_TIMEOUT

def write_token_to_aws(token):
    payload = { 'token': token }
    req = requests.post(POST_TOKEN_URL, json=payload)
    res = req.json()
    game_id = res['game_id']
    print("GAME_ID = %s" % (game_id))
    return game_id

#Main
if __name__ == '__main__':
    sleep()
    while True:
        if(state != SLEEP_STATE):
            if(has_reached_timeout()):
                sleep()
            elif(state == GAME_STATE):
                if(is_game_over()):
                    print("GAME OVER!")
                    game_over()
            # elif(is_game_over()):
            #     print("GAME OVER!")
            #     game_over()
            # else:
            #     print("GAME NOT OVER")

#Misc todo
# button hold, other options seem like too much work. for now just have it adding one and then subtracting 2
# add aws config to source
# deploy scripts/organize repo
# Game over not working?
# run python program on boot

#Enhancements
# remote buttons/iot buttons
# native apps
# user accounts
# request game in app?
