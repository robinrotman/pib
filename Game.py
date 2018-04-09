from gpiozero import Button
import time
import boto3
import random
import requests

BUTTON1_GPIO = 4
BUTTON2_GPIO = 5
BUTTON3_GPIO = 6
BUTTON_HOLD_TIME = 3
SLEEP_TIMEOUT = 15 * 60

SLEEP_STATE: 'sleep',
SETUP_STATE: 'setup',
ONLINE_SETUP_STATE: 'online_setup',
GAME_STATE: 'game',
GAME_OVER_STATE: 'game_over'

button1 = Button(BUTTON1_GPIO)
button2 = Button(BUTTON2_GPIO)
button3 = Button(BUTTON3_GPIO)

button1.hold_time, button2.hold_time, button3.hold_time = BUTTON_HOLD_TIME

time_of_last_interaction = time.time()
game_id = None
state = SLEEP_STATE
play_to_score = 25
scores = [0, 0]

def goto_setup:
    state = SETUP_STATE

def increase_score(player_index):
    time_of_last_interaction = time.time()
    scores[player_index] += 1

def decrease_score(player_index):
    time_of_last_interaction = time.time()
    scores[player_index] -= 1

def increase_player1_score:
    time_of_last_interaction = time.time()
    increase_score(0)

def increase_player2_score:
    time_of_last_interaction = time.time()
    increase_score(1)

def decrease_max_score:
    time_of_last_interaction = time.time()
    play_to_score -= 1

def increase_max_score:
    time_of_last_interaction = time.time()
	play_to_score += 1

def generate_token:
	return random.randomInt(1000, 10000)

def reset:
	time_of_last_interaction = time.time()
	game_id = None
	play_to_score = 25
	scores = [0, 0]

def goto_game:
    state = GAME_STATE

def goto_sleep:
	reset()
	state = SLEEP_STATE
	button1.when_held, button2.when_held, button3.when_held = goto_setup

def is_game_over:
    if ((max(scores) >= play_to_score and has_won_by_two) or max(scores) == 99):
        state = GAME_OVER_STATE
 		if game_id:
 			#write to aws
        #flash winner score and color(?)

def has_won_by_two:
    abs(scores[0] - scores[1]) >= 2

def has_reached_timeout:
    time.time() - time_of_last_interaction >= SLEEP_TIMEOUT

if __name__ == '__main__':
	goto_sleep()
    while True:
	    # sleep state:
	    # When any button held, wake up -> setup state
		if state == SLEEP_STATE:
	        button1.when_held, button2.when_held, button3.when_held = goto_setup

	    elif state == ONLINE_SETUP_STATE:
	    	# generate random 4 digit number (1000 - 9999)
	    	token = generate_token()
	    	# POST /token
	    	# poll GET /game/current - eventually return the game_id
	    	# set game_id variable
	    	# GET /game/{game_id}
	    	# set stat variables locally
	    	# transition to game state

	    #Setup state:
	    #button1: decrease final score
	    #button2: start game
	    #button3: increase final score
	    elif state == SETUP_STATE:
	    	scores = [0, 0]

	    	button1.when_pressed = decrease_max_score
	    	button3.when_pressed = increase_max_score

	        button2.when_held = goto_game

	    #Game state:
	    #button1_press: increase_score(0)
	    #button1_hold: decrease_score(0)
	    #button2_press: XXXXX
	    #button2_hold: go to setup
	    #button3_press: increase_score(1)
	    #button3_hold: decrease_score(1)
	    elif state == GAME_STATE:
	        button1.when_pressed = increase_player1_score
	        button1.when_held = decrease_player1_score
	        button3.when_pressed = increase_player2_score
	        button3.when_held = decrease_player2_score
	        button2.when_held = goto_setup

	        while not is_game_over():
	            #game is running

	    elif state == GAME_OVER_STATE:
	        button1.when_pressed, button1.when_held, button3.when_pressed, button3.when_held = None
	        button2.when_held = goto_setup
	        #send scores to aws
	        #players have 15 minute window to claim game before locking as unassigned

	    if has_reached_timeout():
	    	goto_sleep()

	    #player_has_won?


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
# move state checks out of loop
# have different buttons for quick start and online start
# should quick start just go straight into game mode?
# how to restart with online game?


































