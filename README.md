# pib
Our very own pib-pong scoreboard!

Gettin' pibby with it

# Endpoints
* POST /token - PIB Board sending the one-time (15 minute) token needed to start a game
  * Return the game_id
* GET /token/{token} - validate the token, returns the game_id if valid
* POST /game - used by the web app to create a game record with the players and the play_to_score
* POST /game/{game_id} - set final game stats
* GET /game/{game_id} - get the game stats to be used to set up the game on the PIB
* GET /leaderboard - get the leaderboard


# Todo
* SET API_BASE_URL env var on pib
* Game over not working?
  * casted the play_to_score from response to an int. did that work?
  * do I need to do long(time.time())?
* Add authorization to api
* button hold, other options seem like too much work. for now just have it adding one and then subtracting 2
* run python program on boot
* add aws config to source
* create deploy scripts

# Future Enhancements
* remote buttons/iot buttons
* user accounts
* native apps
  * request game in app?
