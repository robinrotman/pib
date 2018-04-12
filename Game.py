from gpiozero import Button
import time
import boto3
import random
import requests
import Scoreboard

BUTTON1_GPIO = 4
BUTTON2_GPIO = 5
BUTTON3_GPIO = 6
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

button1.hold_time, button2.hold_time, button3.hold_time = BUTTON_HOLD_TIME

scoreboard = Scoreboard('red', 'blue')
time_of_last_interaction = time.time()
game_id = None
state = SLEEP_STATE
play_to_score = 25
scores = [0, 0]

def setup():
    reset_buttons()
    state = SETUP_STATE
    scores = [0, 0]
    button1.when_pressed = decrease_max_score
    button3.when_pressed = increase_max_score
    button2.when_held = play_game

def increase_score(player_index):
    time_of_last_interaction = time.time()
    scores[player_index] += 1
    scoreboard.show_score(scores[0], scores[1])

def decrease_score(player_index):
    time_of_last_interaction = time.time()
    scores[player_index] -= 1
    scoreboard.show_score(scores[0], scores[1])

def increase_player1_score():
    time_of_last_interaction = time.time()
    increase_score(0)

def increase_player2_score():
    time_of_last_interaction = time.time()
    increase_score(1)

def decrease_max_score():
    time_of_last_interaction = time.time()
    play_to_score -= 1

def increase_max_score():
    time_of_last_interaction = time.time()
    play_to_score += 1

def generate_token():
    return random.randomInt(1000, 10000)

def reset():
    time_of_last_interaction = time.time()
    game_id = None
    play_to_score = 25
    scores = [0, 0]

def reset_buttons():
    button1.when_pressed, button2.when_pressed, button3.when_pressed = None
    button1.when_held, button2.when_held, button3.when_held = None

def play_game():
    reset_buttons()
    state = GAME_STATE
    button1.when_pressed = increase_player1_score
    button1.when_held = decrease_player1_score
    button3.when_pressed = increase_player2_score
    button3.when_held = decrease_player2_score
    button2.when_held = setup

def game_over():
    reset_buttons()
    state = GAME_OVER_STATE
    button1.when_pressed, button1.when_held, button2.when_pressed, button3.when_pressed, button3.when_held = None
    button2.when_held = setup
    if game_id:
        #write to aws
    #flash score and winner color

def sleep():
    reset_buttons()
    reset()
    state = SLEEP_STATE
    button1.when_held = play_game_if_both_pressed
    button2.when_held = setup_online

def play_game_if_both_pressed():
    if(button1.is_pressed() and button3.is_pressed()):
        play_game()

def setup_online():
    token = generate_token()
    token_as_scores = token_to_score_list(token)
    #write to aws
    show_score(token_as_scores[0], token_as_scores[1])
    # TODO: FINISH THIS

def token_to_score_list(token):
    return [token / 100, token % 100]

def is_game_over():
    return ((max(scores) >= play_to_score and has_won_by_two) or max(scores) == 99)

def has_won_by_two():
    abs(scores[0] - scores[1]) >= 2

def has_reached_timeout():
    return time.time() - time_of_last_interaction >= SLEEP_TIMEOUT

if __name__ == '__main__':
    sleep()
    while True:
        while (state != SLEEP_STATE):
            if(has_reached_timeout()):
                sleep()
                break
            elif(is_game_over()):
                game_over()


#Endpoints
# POST /token - PIB Board sending the one-time (15 minute) token needed to start a game
# GET /game/current - endpoint to poll to get the game_id of the online setup game
  # Return the game_id
# POST /game - create a new game (use for quick start only)
  # Return the game_id
# POST /game/{game_id} - send final game stats
# GET /game/{game_id} - get the game stats to be used to set up the game on the PIB



#Web app
# Setup Page
# # Player1: email text input (verifier: ends with "@thelevelup.com")
# # Player2: email text input (verifier: ends with "@thelevelup.com")
# # Max Score: integer (verifier 1-99)
# # Player1 Color: drop down text rgb color
# # Player2 Color: drop down text rgb color

# Leaderboard Page
# sorted descending by winslist of {Player Name} - {Number of wins} - {Number of losses}
# |Place|Name|Wins|Losses|Ratio|



#AWS todo
# Database table with games
# (Leaderboard database)



#Misc todo
# finish online_setup
# how to restart with online game?
# cleanup file


































