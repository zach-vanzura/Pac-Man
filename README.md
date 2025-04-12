# Software Engineering Digital Pac-Man Redition
# Lila Mcguirk, Alexa Witkin, Zach Vanzura, Ashton Putnam

# Overview of the rules of Pac-Man:
- The main goal in Pac-Man is to eat all the pellets in the maze while avoiding the ghosts.
  After successfully eating all the pellets, the player will advance to the next level.
- To move Pac-Man, use the arrow keys.
- Pellets are worth 10 points, energizers are worth 50 points and turn the ghosts blue for a few seconds, so you can eat them,
  and fruits appear around the map and are worth bonus points.
- The game ends when the player either run out of lives or when the "esc" button is pushed, which will exit the game and prompt the player to input their initials and their score will be saved.

# How to run our program: 
- Run my_flask.py. From there you can click the "play" button which will allow you to play the game.

# Overview of "final-spring-start-point":
- test.py contains the logic of the game and brings all the individual pieces (pacman, ghosts, pellets, tiles, fruit, etc.) together.
- tile.py creates the tile objects that the map is composed of.
- my_flask.py holds the python flask and is designed in index.html which is stored in the "templates" folder.
- pacman_store.db holds the database where the player score are kept.
