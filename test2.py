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


class Controllable(arcade.Sprite):
    # TODO: It may be wise to add an is_player boolean but we could also just make the first controllable the player
    def __init__(self, path_to_sprite, scale, window_width, window_height):
        super().__init__(path_to_sprite, scale=scale)
        self.center_x = window_width / 2
        self.center_y = window_height / 2
        self.window_width, self.window_height = window_width, window_height
        self.is_edible = False

    def update(self, delta_time: float = 1 / 60):
        """ Move the Player Sprite """
        # Move player
        # Remove these lines if physics engine is moving player
        self.center_x += self.change_x
        self.center_y += self.change_y

        # sprites will wrap around the screen
        if self.left < 0:
            self.right = self.window_width - 1
        elif self.right > self.window_width - 1:
            self.left = 0

        if self.bottom < 0:
            self.top = self.window_height - 1
        elif self.top > self.window_height - 1:
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
        target_tile = self.get_target_tile()
        target_x = target_tile[0] * TILE_SIZE
        target_y = target_tile[1] * TILE_SIZE
        
        if self.center_x < target_x:
            self.center_x += GHOST_SPEED
        elif self.center_x > target_x:
            self.center_x -= GHOST_SPEED
        
        if self.center_y < target_y:
            self.center_y += GHOST_SPEED
        elif self.center_y > target_y:
            self.center_y -= GHOST_SPEED

        # Call the parent update method to handle screen wrapping
        super().update(delta_time)


class Player(Controllable):
    def __init__(self, path_to_sprite, scale, window_width, window_height):
        super().__init__(path_to_sprite, scale, window_width, window_height)
        self.is_dead = False


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        """ Initializer """
        super().__init__()

        # Variables that will hold sprite lists
        self.player_list = None
        self.ghost_list = None
        self.wall_list = None

        # Set up the player info
        self.player_sprite = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.physics_engine = None

        # Set background color
        self.background_color = arcade.color.BLACK

    def setup(self):
        """ Set up the game and initialize the variables """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()

        self.wall_list = arcade.SpriteList(use_spatial_hash=True,
                                           spatial_hash_cell_size=128)

        # Set up the player
        self.player_sprite = Player("images/pacman.png", scale=SPRITE_SCALING, 
                                    window_width=WINDOW_WIDTH, window_height=WINDOW_HEIGHT)
        self.player_sprite.center_x = WINDOW_WIDTH / 2
        self.player_sprite.center_y = (WINDOW_HEIGHT / 2) - 200
        self.player_list.append(self.player_sprite)

        # Ghost image file paths and types in corresponding order
        ghost_images = [
            "images/blinky.png",
            "images/inky.png",
            "images/pinky.png",
            "images/clyde.png"
        ]
        ghost_types = ["Blinky", "Inky", "Pinky", "Clyde"]

        # Create a temporary list to store ghost instances, to allow linking Inky with Blinky later
        temp_ghosts = []

        # Set up the ghosts
        for i in range(4):
            # For now, we pass None for blinky. Later, we assign it if needed.
            ghost_sprite = Ghost(ghost_images[i], scale=GHOST_SCALING, 
                                 ghost_type=ghost_types[i], player=self.player_sprite)
            ghost_sprite.center_x = WINDOW_WIDTH / 2 + (i * 50) - 75  # Spread ghosts horizontally
            ghost_sprite.center_y = (WINDOW_HEIGHT / 2) + 200
            self.ghost_list.append(ghost_sprite)
            temp_ghosts.append(ghost_sprite)

        # Assign Blinky reference for Inky (assuming Blinky is the first ghost)
        for ghost in temp_ghosts:
            if ghost.ghost_type == "Inky":
                ghost.blinky = temp_ghosts[0]

        # Set up the walls
        spacing = SPRITE_SIZE * 3
        for column in range(10):
            for row in range(15):
                sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png",
                                       scale=SPRITE_SCALING)
                x = (column + 1) * spacing
                y = (row + 1) * sprite.height
                sprite.center_x = x
                sprite.center_y = y
                if random.randrange(100) > 30:
                    self.wall_list.append(sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         self.wall_list)

    def on_draw(self):
        """ Render the screen """
        self.clear()
        self.player_list.draw()
        self.ghost_list.draw()
        self.wall_list.draw()
        

    def update_player_speed(self):
        """ Calculate speed based on the keys pressed """
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
        """ All the logic to move, and the game logic goes here """
        self.player_list.update(delta_time)
        self.ghost_list.update(delta_time)

    def on_key_press(self, key, key_modifiers):
        """ Called whenever a key on the keyboard is pressed """
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
        """ Called whenever the user lets off a previously pressed key """
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
    """ Main function """
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    game.setup()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()