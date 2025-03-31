"""
CS3050: Software Engineering
Final Project -> Pac-Man inspired game

Group Members:
    Lila Mcguirk
    Ashton Putnam
    Zach Vanzura
    Alexa Witkin
"""

"""
Notes:
Pac-Man uses a 5:4 window ratio
pixel width = pixel height * 1.25
for now, 900px = 720px * 1.25
"""

import arcade
import random
import math

# Constants
SPRITE_SCALING = 0.025
GHOST_SCALING = 0.075
SPRITE_SIZE = 32
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 720
PACMAN_SPEED = 5
GHOST_SPEED = 2
TILE_SIZE = 36  # Adjusted to fit the 900x720 window properly
WINDOW_TITLE = "PAC-MAN"

# New constant for wall scaling.
# Assuming the wall sprite has an original size of 128 pixels,
# scaling it so that each wall fits the TILE_SIZE.
WALL_SCALING = TILE_SIZE / 128

# -----------------------------------------------------------------------------
# Helper function to draw a rectangle outline (for older versions of Arcade)
# -----------------------------------------------------------------------------
def draw_rectangle_outline(center_x, center_y, width, height, color, border_width=1):
    left = center_x - width / 2
    right = center_x + width / 2
    top = center_y + height / 2
    bottom = center_y - height / 2
    arcade.draw_line(left, top, right, top, color, border_width)
    arcade.draw_line(right, top, right, bottom, color, border_width)
    arcade.draw_line(right, bottom, left, bottom, color, border_width)
    arcade.draw_line(left, bottom, left, top, color, border_width)

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------
class Controllable(arcade.Sprite):
    def __init__(self, path_to_sprite, scale, window_width, window_height):
        super().__init__(path_to_sprite, scale=scale)
        self.center_x = window_width / 2
        self.center_y = window_height / 2
        self.window_width, self.window_height = window_width, window_height
        self.is_edible = False

    def update(self, delta_time: float = 1 / 60):
        # This method is not used for movement anymore since physics engine update
        # now handles the player collision.
        """ Wrap around the screen if the sprite moves out of bounds """
        if self.left < 0:
            self.right = self.window_width
        elif self.right > self.window_width:
            self.left = 0

        if self.bottom < 0:
            self.top = self.window_height
        elif self.top > self.window_height:
            self.bottom = 0

class Ghost(arcade.Sprite):
    def __init__(self, path_to_sprite, scale, ghost_type, player, blinky=None):
        super().__init__(path_to_sprite, scale=scale)
        self.ghost_type = ghost_type
        self.player = player
        self.blinky = blinky  # Needed for Inky's logic

    def get_target_tile(self):
        pacman_tile = (self.player.center_x // TILE_SIZE, self.player.center_y // TILE_SIZE)
        
        if self.ghost_type == "Blinky":
            return pacman_tile
        
        elif self.ghost_type == "Pinky":
            offset_x = math.cos(math.radians(self.player.angle)) * 4
            offset_y = math.sin(math.radians(self.player.angle)) * 4
            return (pacman_tile[0] + offset_x, pacman_tile[1] + offset_y)
        
        elif self.ghost_type == "Inky" and self.blinky:
            blinky_tile = (self.blinky.center_x // TILE_SIZE, self.blinky.center_y // TILE_SIZE)
            vector_x = (pacman_tile[0] - blinky_tile[0]) * 2
            vector_y = (pacman_tile[1] - blinky_tile[1]) * 2
            return (blinky_tile[0] + vector_x, blinky_tile[1] + vector_y)
        
        elif self.ghost_type == "Clyde":
            distance = math.sqrt((self.center_x - self.player.center_x) ** 2 + (self.center_y - self.player.center_y) ** 2)
            if distance > TILE_SIZE * 8:
                return pacman_tile
            else:
                return (5, 5)  # Clyde's corner
        
        return pacman_tile
    
    def update(self, delta_time: float = 1 / 60):
        """
        Instead of directly changing the sprite's position, we update change_x and change_y.
        The physics engine for ghosts will use these values to move the ghost and check collisions.
        """
        target_tile = self.get_target_tile()
        target_x = target_tile[0] * TILE_SIZE
        target_y = target_tile[1] * TILE_SIZE
        
        # Determine horizontal movement
        if self.center_x < target_x:
            self.change_x = GHOST_SPEED
        elif self.center_x > target_x:
            self.change_x = -GHOST_SPEED
        else:
            self.change_x = 0
        
        # Determine vertical movement
        if self.center_y < target_y:
            self.change_y = GHOST_SPEED
        elif self.center_y > target_y:
            self.change_y = -GHOST_SPEED
        else:
            self.change_y = 0

class Player(Controllable):
    def __init__(self, path_to_sprite, scale, window_width, window_height):
        super().__init__(path_to_sprite, scale, window_width, window_height)
        self.is_dead = False

class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__()
        self.player_list = None
        self.ghost_list = None
        self.wall_list = None
        self.player_sprite = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.physics_engine = None
        self.ghost_physics_engines = []  # Physics engines for ghosts
        self.background_color = arcade.color.BLACK

    def setup(self):
        """ Set up the game and initialize the variables """
        self.player_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=128)

        # Set up the player. The player's movement is handled by a physics engine.
        self.player_sprite = Player("images/pacman.png", scale=SPRITE_SCALING, 
                                    window_width=WINDOW_WIDTH, window_height=WINDOW_HEIGHT)
        self.player_sprite.center_x = WINDOW_WIDTH / 2
        self.player_sprite.center_y = (WINDOW_HEIGHT / 2) - 200
        self.player_list.append(self.player_sprite)

        ghost_images = [
            "images/blinky.png",
            "images/inky.png",
            "images/pinky.png",
            "images/clyde.png"
        ]
        ghost_types = ["Blinky", "Inky", "Pinky", "Clyde"]

        temp_ghosts = []
        for i in range(4):
            ghost_sprite = Ghost(ghost_images[i], scale=GHOST_SCALING, 
                                 ghost_type=ghost_types[i], player=self.player_sprite)
            ghost_sprite.center_x = WINDOW_WIDTH / 2 + (i * 50) - 75
            ghost_sprite.center_y = (WINDOW_HEIGHT / 2) + 200
            self.ghost_list.append(ghost_sprite)
            temp_ghosts.append(ghost_sprite)

        for ghost in temp_ghosts:
            if ghost.ghost_type == "Inky":
                ghost.blinky = temp_ghosts[0]

        # Set up the maze walls from A-star_pathfinding.py
        self.setup_maze_walls()

        # Create physics engine for the player so that movement is collision checked.
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        # Create a physics engine for each ghost.
        self.ghost_physics_engines = []
        for ghost in self.ghost_list:
            engine = arcade.PhysicsEngineSimple(ghost, self.wall_list)
            self.ghost_physics_engines.append(engine)

    def setup_maze_walls(self):
        """
        Set up the maze walls based on a grid layout.
        'X' represents a wall and ' ' represents an open space.
        The maze is centered in the window.
        """
        maze = [
            "XXXXXXXXX  XXXXXXXXXXXX",
            "X                     X",
            "X                     X",
            "X   XXXXX    XXXXXX   X",
            "        X    X         ",
            "        X    X         ",
            "X   XXXXX    XXXXXX   X",
            "X                     X",
            "X                     X",
            "XXXXXXXXXX  XXXXXXXXXXX"
        ]
        rows = len(maze)
        cols = len(maze[0])
        offset_x = (WINDOW_WIDTH - (cols * TILE_SIZE)) / 2
        offset_y = (WINDOW_HEIGHT - (rows * TILE_SIZE)) / 2

        for row_index, row in enumerate(maze):
            for col_index, char in enumerate(row):
                if char == "X":
                    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", scale=WALL_SCALING)
                    wall.center_x = col_index * TILE_SIZE + TILE_SIZE / 2 + offset_x
                    wall.center_y = (rows - row_index - 1) * TILE_SIZE + TILE_SIZE / 2 + offset_y
                    self.wall_list.append(wall)

    def on_draw(self):
        """ Render the screen """
        self.clear()
        self.player_list.draw()
        self.ghost_list.draw()
        self.wall_list.draw()

        # Draw a thin border around each wall tile using our custom function
        for wall in self.wall_list:
            draw_rectangle_outline(wall.center_x, wall.center_y, wall.width, wall.height,
                                   color=arcade.color.WHITE, border_width=1)

    def update_player_speed(self):
        """ Calculate speed based on the keys pressed. For the player, this updates change_x and change_y. """
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = PACMAN_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PACMAN_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PACMAN_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PACMAN_SPEED

    def on_update(self, delta_time):
        """
        Update the game logic.
        The player's movement is updated via its physics engine.
        Each ghost's update method sets its desired movement, which is then applied via its own physics engine.
        """
        # Update player's movement with collision detection.
        self.update_player_speed()
        self.physics_engine.update()

        # Update ghosts' movement logic (which sets change_x and change_y)
        for ghost in self.ghost_list:
            ghost.update(delta_time)
        # Then update each ghost's physics engine to enforce collisions.
        for engine in self.ghost_physics_engines:
            engine.update()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        self.update_player_speed()

    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        self.update_player_speed()

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    game.setup()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()