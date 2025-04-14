# Software Engineering Digital Pac-Man Redition
# Lila Mcguirk, Alexa Witkin, Zach Vanzura, Ashton Putnam

# Overview of the rules of Pac-Man:
- The main goal in Pac-Man is to eat all the pellets in the maze while avoiding the ghosts.
  After successfully eating all the pellets, the player will advance to the next level. Our version of the game has the player try to achieve as high a score as possible by eating pellets, fruits, and ghosts.
- To move Pac-Man, use the arrow keys.
- Pellets are worth 10 points, energizers are worth 50 points, the ghosts turn blue for a few seconds after the player eats an energizer pellet so you can eat them to get 200 points, and fruits appear around the map and are worth bonus points.
- The game ends when the player either runs out of lives or when the "esc" button is pushed, which will exit the game and prompt the player to input their initials and their score will be saved.

# How to run our program: 
- Run my_flask.py. From there you can click the "play" button within the webpage which will allow you to play the game.

# Overview of "final-spring-start-point":
- test.py contains the logic of the game and brings all the individual pieces (pacman, ghosts, pellets, tiles, fruit, etc.) together. 
- tile.py creates the tile objects that the map is composed of.
- my_flask.py holds the python flask and is designed in index.html which is stored in the "templates" folder.
- pacman_store.db holds the database where the player score are kept.
- controllable.py contains the class declarations for the controllable objects (pacman and ghosts). This file contains most of the AI logic for the ghosts, the player movement logic, and pac-man animation. 
- consumable.py contains the class declarations for the consumable objects (pellets and fruit). This file contains the logic for the pellets and fruit.

# Citations
https://www.deviantart.com/darthbladerpegasus/art/Pac-Man-Arcade-Logo-959562739
https://pacman.fandom.com/wiki/Pac-Man
https://tvtropes.org/pmwiki/pmwiki.php/Characters/PacMan
https://ksagar.com/?k=249672015
https://www.pngall.com/pacman-ghost-png/download/172942/ (adjusted colors for other ghosts)