# pib
Our very own pib-pong scoreboard!

Gettin' pibby with it

# Endpoints
* POST /token - PIB Board sending the one-time (15 minute) token needed to start a game
  * Return the game_id
* POST /game/{game_id} - send final game stats
* GET /game/{game_id} - get the game stats to be used to set up the game on the PIB