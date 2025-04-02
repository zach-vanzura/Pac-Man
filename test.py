# TODO: Begin using pylint

import arcade
from consumables.apple import Apple
from consumables.bell import Bell
from controllable import Controllable
from consumables.cherry import Cherry
from consumables.galaxian import Galaxian
from consumables.pellet_energizer import EnergizerPellet as Energizer
# from consumables.key import Key
from consumables.melon import Melon
from consumables.orange import Orange
from consumables.pellet_small import Pellet
from consumables.strawberry import Strawberry
from tile import *

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
Based on Starting Template Using Window Class in the PyArcade Docs
Additionally, added components from Better Move By Keyboard

https://api.arcade.academy/en/latest/example_code/starting_template.html#starting-template
https://api.arcade.academy/en/latest/example_code/sprite_move_keyboard_better.html#sprite-move-keyboard-better

Got the Pac-Man sprite from:
https://www.stickpng.com/img/games/pac-man/pac-man-plain-yellow


- Ashton
"""


# TODO: create mazes, create start menu screen, add animations, add enemy sprites,
# add enemy movement and attacking, add settings menu, add alternative sprites (Jason's face),
# add various menus/start screens/end screens (look up what is actually in pacman),
# etc...

# Set tile size, window height and width
TILE_SIZE = 24
WINDOW_WIDTH = 28 * TILE_SIZE  # 28 columns
WINDOW_HEIGHT = 36 * TILE_SIZE  # 36 rows

# Set window title
WINDOW_TITLE = "PAC-MAN"

# Set player movement speed
MOVEMENT_SPEED = 5

class Symbols(Enum):
    PELLET = '.'
    ENERGIZER = 'o'
    EMPTY_SPACE = '#'


tile_textures = [
    "############################",
    "############################",
    "############################",
    "C============PP============C",
    "=............||............=",
    "=.L||L.L|||L.||.L|||L.L||L.=",
    "=o|##|.|###|.||.|###|.|##|o=",
    "=.L||L.L|||L.LL.L|||L.L||L.=",
    "=..........................=",
    "=.L||L.LL.L||||||L.LL.L||L.=",
    "=.L||L.||.L||LL||L.||.L||L.=",
    "=......||....||....||......=",
    "C====L.|L||L#||#L||L|.L====C",
    "#####=.|L||L#LL#L||L|.=#####",
    "#####=.||##########||.=#####",
    "#####=.||#j==__==j#||.=#####",
    "=====L.LL#=######=#LL.L=====",
    "######.###=######=###.######",
    "=====L.LL#=######=#LL.L=====",
    "#####=.||#j======j#||.=#####",
    "#####=.||##########||.=#####",
    "#####=.||#L||||||L#||.=#####",
    "C====L.LL#L||LL||L#LL.L====C",
    "=............||............=",
    "=.L||L.L|||L.||.L|||L.L||L.=",
    "=.L|L|.L|||L.LL.L|||L.|L|L.=",
    "=o..||.......##.......||..o=",
    "H|L.||.LL.L||||||L.LL.||.L|H",
    "H|L.LL.||.L||LL||L.||.LL.L|H",
    "=......||....||....||......=",
    "=.L||||LL||L.||.L||LL||||L.=",
    "=.L||||||||L.LL.L||||||||L.=",
    "=..........................=",
    "C==========================C",
    "############################",
    "############################",
]

tile_orientations = [
    "############################",
    "############################",
    "############################",
    "y0000000000000y0000000000000",
    "Y............TT............T",
    "Y.y000.y0000.TT.y0000.y000.T",
    "YoT##T.T###T.TT.T###T.T##ToT",
    "Y.z00x.z000x.zx.z000x.z00x.T",
    "Y..........................T",
    "Y.y000.y0.y0000000.y0.y000.T",
    "Y.z00x.TT.z000y00x.TT.z00x.T",
    "Y......TT....TT....TT......T",
    "zxxxx0.Tz000#TT#y00xT.yxxxxx",
    "#####Y.Ty00x#zx#z000T.T#####",
    "#####Y.TT##########TT.T#####",
    "#####Y.TT#yxx00xx0#TT.T#####",
    "00000x.zx#T######Y#zx.z00000",
    "######.###T######Y###.######",
    "xxxxx0.y0#T######Y#y0.yxxxxx",
    "#####Y.TT#z000000x#TT.T#####",
    "#####Y.TT##########TT.T#####",
    "#####Y.TT#y0000000#TT.T#####",
    "y0000x.zx#z000y00x#zx.z00000",
    "Y............TT............T",
    "Y.y000.y0000.TT.y0000.y000.T",
    "Y.z00T.z000x.zx.z000x.Ty0x.T",
    "Yo..TT.......##.......TT..oT",
    "z00.TT.y0.y0000000.y0.TT.y0x",
    "y0x.zx.TT.z000y00x.TT.zx.z00",
    "Y......TT....TT....TT......T",
    "Y.y0000xz000.TT.y00xz00000.T",
    "Y.z00000000x.zx.z00000000x.T",
    "Y..........................T",
    "zxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "############################",
    "############################",
]

class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        """ Initializer """

        # Call the parent class initializer
        super().__init__()

        # Variables that will hold sprite lists
        self.controllable_list = None
        self.tile_list = None
        self.to_be_eaten = None

        # Set up the player info
        self.player_sprite = None
        self.tile_sprite = None  # pellets wil be added to the tile sprite list
        self.consumable_sprite = None  # we probably don't need sprites for every fruit

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        # fixme: pressing the esc key doesn't close the window yet
        self.esc_pressed = False

        # Set background color
        self.background_color = arcade.color.BLACK

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        self.controllable_list = arcade.SpriteList()
        self.consumable_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()


        # TODO: add textures and orientations maps

        # TODO: set up pacman

        # TODO: add loops to generate tiles

        # TODO: KEEP TRACK OF SCORE WHEN PELLETS ARE EATEN
        #
        # offset_x = TILE_SIZE // 2
        # offset_y = TILE_SIZE // 2
        #
        # for row_index, row in enumerate(pellet_map):
        #     for col_index, tile in enumerate(row):
        #         x = col_index * TILE_SIZE + offset_x
        #         y = (len(pellet_map) - row_index - 1) * TILE_SIZE + offset_y
        #
        #         # small pellet
        #         if tile == ".":
        #             self.pellet_sprite = Pellet("images/pellet.png", 0.05, WINDOW_WIDTH, WINDOW_HEIGHT)
        #             self.pellet_sprite.center_x = x
        #             self.pellet_sprite.center_y = y
        #             self.consumable_list.append(self.pellet_sprite)
        #
        #         # energizer
        #         if tile == "-":
        #             self.energizer_pellet_sprite = Energizer("images/pellet.png", 0.1, WINDOW_WIDTH, WINDOW_HEIGHT)
        #             self.energizer_pellet_sprite.center_x = x
        #             self.energizer_pellet_sprite.center_y = y
        #             self.consumable_list.append(self.energizer_pellet_sprite)
        #
        #         # cherry
        #         if tile == "c":
        #             self.cherry_sprite = Cherry("images/cherry.png", 0.07, WINDOW_WIDTH, WINDOW_HEIGHT)
        #             self.cherry_sprite.center_x = x
        #             self.cherry_sprite.center_y = y
        #             self.consumable_list.append(self.cherry_sprite)
        #
        #         # strawberry
        #         if tile == "s":
        #             self.strawberry_sprite = Strawberry("images/strawberry.png", 0.09, WINDOW_WIDTH, WINDOW_HEIGHT)
        #             self.strawberry_sprite.center_x = x
        #             self.strawberry_sprite.center_y = y
        #             self.consumable_list.append(self.strawberry_sprite)
        #
        #         # orange
        #         if tile == "o":
        #             self.orange_sprite = Orange("images/orange.png", 0.07, WINDOW_WIDTH, WINDOW_HEIGHT)
        #             self.orange_sprite.center_x = x
        #             self.orange_sprite.center_y = y
        #             self.consumable_list.append(self.orange_sprite)
        #
        #         # apple
        #         if tile == "a":
        #             self.apple_sprite = Apple("images/apple.png", 0.1, WINDOW_WIDTH, WINDOW_HEIGHT)
        #             self.apple_sprite.center_x = x
        #             self.apple_sprite.center_y = y
        #             self.consumable_list.append(self.apple_sprite)
        #
        #         # melon
        #         if tile == "m":
        #             self.melon_sprite = Melon("images/melon.png", 0.1, WINDOW_WIDTH, WINDOW_HEIGHT)
        #             self.melon_sprite.center_x = x
        #             self.melon_sprite.center_y = y
        #             self.consumable_list.append(self.melon_sprite)
        #
        #         # galaxian
        #         if tile == "g":
        #             self.galaxian_sprite = Galaxian("images/galaxian.png", 0.1, WINDOW_WIDTH, WINDOW_HEIGHT)
        #             self.galaxian_sprite.center_x = x
        #             self.galaxian_sprite.center_y = y
        #             self.consumable_list.append(self.galaxian_sprite)
        #
        #         # bell
        #         if tile == "b":
        #             self.bell_sprite = Bell("images/bell.png", 0.08, WINDOW_WIDTH, WINDOW_HEIGHT)
        #             self.bell_sprite.center_x = x
        #             self.bell_sprite.center_y = y
        #             self.consumable_list.append(self.bell_sprite)

                # key
                # if tile == "k":
                #     self.key_sprite = Key("images/key.png", 0.08, WINDOW_WIDTH, WINDOW_HEIGHT)
                #     self.key_sprite.center_x = x
                #     self.key_sprite.center_y = y
                #     self.consumable_list.append(self.key_sprite)

    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.controllable_list.draw()
        self.consumable_list.draw()

    def update_player_speed(self):
        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.controllable_list.update(delta_time)
        # find all sprites tha will collide with the pac man
        self.to_be_eaten = self.player_sprite.collides_with_list(self.consumable_list)
        for sprite in self.to_be_eaten:
            sprite.set_eaten()
            self.player_sprite.score += sprite.score

            # elif sprite == self.key_sprite:
            #     self.player_sprite.score += KEY_VALUE
            print(self.player_sprite.score)
        for sprite in self.consumable_list:
            sprite.update()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        # TODO: change the direction pacman is facing based on key press
        if key == arcade.key.UP:
            self.up_pressed = True
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = True
            self.update_player_speed()
        elif key == arcade.key.LEFT:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
            self.update_player_speed()
        elif key == arcade.key.ESCAPE:
            self.esc_pressed = True

    # TODO: CHANGE LOGIC SO PACMAN CONTINUES MOVING IN THE DIRECTION OF A KEY PRESS EVEN AFTER RELEASE
    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.UP:
            self.up_pressed = False
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = False
            self.update_player_speed()
        elif key == arcade.key.LEFT:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
            self.update_player_speed()
        elif key == arcade.key.ESCAPE:
            self.esc_pressed = False

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass


def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and setup the GameView
    game = GameView()
    game.setup()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()

