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


# Set scale of sprites
SPRITE_SCALING = 0.025
GHOST_SCALING = 0.075

GHOST_COUNT = 4

# Set window height and width in 5:4 ratio
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 720

# Set window title
WINDOW_TITLE = "PAC-MAN"

# Set player movement speed
PACMAN_SPEED = 5
GHOST_SPEED = 2


class Controllable(arcade.Sprite):
    # TODO: It may be wise to add an is_player boolean but we could also just make the first controllable the player
    def __init__(self, path_to_sprite, scale, window_width, window_height, ):
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


class Ghost(Controllable):
    def __init__(self, path_to_sprite, scale, window_width, window_height, player_sprite):
        super().__init__(path_to_sprite, scale, window_width, window_height)
        self.is_edible = False
        self.player_sprite = player_sprite

    def update(self, delta_time: float = 1 / 60):
        """ Move the Ghost Sprite """
        if self.center_y < self.player_sprite.center_y:
            self.center_y += min(GHOST_SPEED, self.player_sprite.center_y - self.center_y)
        elif self.center_y > self.player_sprite.center_y:
            self.center_y -= min(GHOST_SPEED, self.center_y - self.player_sprite.center_y)

        if self.center_x < self.player_sprite.center_x:
            self.center_x += min(GHOST_SPEED, self.player_sprite.center_x - self.center_x)
        elif self.center_x > self.player_sprite.center_x:
            self.center_x -= min(GHOST_SPEED, self.center_x - self.player_sprite.center_x)

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

        # Set up the player info
        self.player_sprite = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Set background color
        self.background_color = arcade.color.BLACK


    def setup(self):
        """ Set up the game and initialize the variables """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player("images/pacman.png", scale=SPRITE_SCALING, 
                                    window_width=WINDOW_WIDTH, window_height=WINDOW_HEIGHT)
        self.player_sprite.center_x = WINDOW_WIDTH / 2
        self.player_sprite.center_y = (WINDOW_HEIGHT / 2) - 200
        self.player_list.append(self.player_sprite)

        # Ghost image file paths
        ghost_images = [
            "images/blinky.png",
            "images/inky.png",
            "images/pinky.png",
            "images/clyde.png"
        ]

        # Set up the ghosts
        for i in range(4):
            ghost_sprite = Ghost(ghost_images[i], scale=GHOST_SCALING, 
                                    window_width=WINDOW_WIDTH, window_height=WINDOW_HEIGHT,
                                    player_sprite=self.player_sprite)
            ghost_sprite.center_x = WINDOW_WIDTH / 2 + (i * 50) - 75  # Spread ghosts horizontally
            ghost_sprite.center_y = (WINDOW_HEIGHT / 2) + 200
            self.ghost_list.append(ghost_sprite)


    def on_draw(self):
        """ Render the screen """
        self.clear()
        self.player_list.draw()
        self.ghost_list.draw()


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