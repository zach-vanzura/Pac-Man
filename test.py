# TODO: Begin using pylint

import arcade
from consumables.apple import Apple
from consumables.bell import Bell
from controllable import *
from consumables.cherry import Cherry
from consumables.galaxian import Galaxian
from consumables.pellet_energizer import EnergizerPellet as Energizer
# from consumables.key import Key
from consumables.melon import Melon
from consumables.orange import Orange
from consumables.pellet_small import Pellet
from consumables.strawberry import Strawberry
from tile import *
import sqlite3 # included in standard python distribution
import pandas as pd

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


# TODO: create start menu screen, add animations, add enemy sprites,
# add enemy movement and attacking, add settings menu, add alternative sprites (Jason's face),
# add various menus/start screens/end screens (look up what is actually in pacman),
# etc...

# Set tile size, window height and width
TILE_SIZE = 24
NUM_ROWS = 36
NUM_COLS = 28
SCREEN_HEIGHT = NUM_ROWS * TILE_SIZE  # 36 rows
SCREEN_WIDTH = NUM_COLS * TILE_SIZE  # 28 columns

# Set window title
WINDOW_TITLE = "PAC-MAN"

# Set player movement speed
MOVEMENT_SPEED = 2

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
    "##############+#############",
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

can_move_tiles = ['o', '.', '#']


def in_bounds(row, col):
    """
    :param row: the row of the maze
    :param col: the column of the maze
    :return: the character at the given row, col index if there is one
    """

    if 0 <= row < NUM_ROWS and 0 <= col < NUM_COLS:
        return tile_textures[row][col]
    return None  # out-of-bounds, treat as wall


class GameView(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        """ Initializer """

        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, 'Pac Man')

        # Variables that will hold sprite lists
        self.curr_row = None
        self.wall_collisions = None
        self.controllable_list = None
        self.tile_list = None
        self.consumable_list = None
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
        self.buffered_key = False
        self.esc_pressed = False

        # Set background color
        self.background_color = arcade.color.BLACK

        self.physics_engine = None

    def setup(self):
        # initialize lists
        self.tile_list = arcade.SpriteList(use_spatial_hash=True)
        self.consumable_list = arcade.SpriteList()
        self.controllable_list = arcade.SpriteList()
        self.to_be_eaten = arcade.SpriteList()

        self.player_sprite = Controllable(os.path.join('images', 'pacman-static.png'), TILE_SIZE)
        self.player_sprite.center_x = TILE_SIZE * 14  # 14 is the x midpoint in the grid
        self.player_sprite.center_y = TILE_SIZE * 9 + TILE_SIZE // 2
        self.controllable_list.append(self.player_sprite)

        # Center of the screen (spawn room)
        spawn_x = SCREEN_WIDTH // 2
        spawn_y = SCREEN_HEIGHT // 2

        # Create ghosts with AI
        self.blinky = Ghost("images/blinky.png", "Blinky", self.player_sprite, self.tile_list)
        self.pinky = Ghost("images/pinky.png", "Pinky", self.player_sprite, self.tile_list)
        self.inky = Ghost("images/inky.png", "Inky", self.player_sprite, self.tile_list, blinky=self.blinky)
        self.clyde = Ghost("images/clyde.png", "Clyde", self.player_sprite, self.tile_list)

        # Position them staggered in spawn room
        offsets = [-TILE_SIZE, 0, TILE_SIZE, TILE_SIZE * 2]
        for i, ghost in enumerate([self.blinky, self.pinky, self.inky, self.clyde]):
            ghost.center_x = spawn_x + offsets[i]
            ghost.center_y = spawn_y

        self.ghosts = arcade.SpriteList()
        self.ghosts.extend([self.blinky, self.pinky, self.inky, self.clyde])

        # go through the two lists to get each tile texture and orientation
        center_y = SCREEN_HEIGHT - TILE_SIZE // 2
        for row in (range(len(tile_textures))):  # iterate over y-axis
            center_x = TILE_SIZE // 2  # reset x pos
            for col in (range(len(tile_textures[0]))):  # iterate over x-axis
                # is pellet
                if tile_textures[row][col] == Symbols.PELLET.value:
                    self.consumable_sprite = Pellet(TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
                    self.consumable_sprite.center_x, self.consumable_sprite.center_y = center_x, center_y
                    self.consumable_list.append(self.consumable_sprite)
                # is energizer
                elif tile_textures[row][col] == Symbols.ENERGIZER.value:
                    self.consumable_sprite = Energizer(TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
                    self.consumable_sprite.center_x, self.consumable_sprite.center_y = center_x, center_y
                    self.consumable_list.append(self.consumable_sprite)
                # is empty space
                elif tile_textures[row][col] == Symbols.EMPTY_SPACE.value:
                    center_x += TILE_SIZE
                    continue
                else:
                    texture = tile_textures[row][col]

                    if texture == '+':
                        self.logo_sprite = arcade.Sprite("images/pac-man-logo.png", scale=0.1)
                        self.logo_sprite.center_x = center_x
                        self.logo_sprite.center_y = center_y + 10

                        # need hasattr or it won't work - adds it to sprite list
                        if not hasattr(self, "logo_list"):
                            self.logo_list = arcade.SpriteList()

                        self.logo_list.append(self.logo_sprite)

                    else:
                        orientation = tile_orientations[row][col]
                        self.tile_sprite = Tile(TILE_SIZE, center_x, center_y, texture, orientation)
                        self.tile_list.append(self.tile_sprite)

                center_x += TILE_SIZE
            center_y -= TILE_SIZE  # increment y position at each level
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.tile_list)

        # Implement Database
        playerId = 1 # alter if additional player is added
        con = sqlite3.connect("pacman_score.db", isolation_level=None)
        cur = con.cursor()
        cur.execute(f'INSERT INTO ScoreBoard (total_score,player) VALUES ("{self.player_sprite.score}", "{playerId}");')
        con.commit()

    def on_draw(self):
        self.clear()
        self.tile_list.draw()
        self.consumable_list.draw()
        # self.tile_list.draw_hit_boxes(color=arcade.color.RED, line_thickness= 1)
        self.controllable_list.draw()
        # self.controllable_list.draw_hit_boxes(color=arcade.color.PINK, line_thickness=1)
        self.ghosts.draw()
        self.logo_list.draw()

    def update_player_speed(self):
        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        if self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_update(self, delta_time=108):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        # position checks before collision checks

        # check the next tile, up, down, left, or right is within bounds
        self.update_curr_tile()
        self.next_y_pos = in_bounds(self.curr_row - 1, self.curr_col)  # going up, decrement index
        self.next_y_neg = in_bounds(self.curr_row + 1, self.curr_col)
        self.next_x_pos = in_bounds(self.curr_row, self.curr_col + 1)
        self.next_x_neg = in_bounds(self.curr_row, self.curr_col - 1)

        if self.up_pressed and self.next_y_pos not in can_move_tiles:
            self.player_sprite.center_y = self.tile_center_y - TILE_SIZE // 4
        if self.down_pressed and self.next_y_neg not in can_move_tiles:
            self.player_sprite.center_y = self.tile_center_y + TILE_SIZE // 4
        if self.left_pressed and self.next_x_neg not in can_move_tiles:
            self.player_sprite.center_x = self.tile_center_x + TILE_SIZE // 4
        if self.right_pressed and self.next_x_pos not in can_move_tiles and self.curr_col != NUM_COLS - 1:  # needed for tunnel
            self.player_sprite.center_x = self.tile_center_x - TILE_SIZE // 4

        self.physics_engine.update()
        self.controllable_list.update(delta_time)
        # find all sprites tha will collide with the pac man
        self.to_be_eaten = self.player_sprite.collides_with_list(self.consumable_list)
        for sprite in self.to_be_eaten:
            # this check isn't really necessary right now, but it may be helpful in the future with ghosts
            if sprite.is_edible:
                sprite.set_eaten()
                self.player_sprite.score += sprite.score
            # fixme: this does NOT work as intended, pacman bounces off walls and does not move smoothly along the maze

            print(self.player_sprite.score)

            # Implement Database
            playerId = 1 # alter if additional player is added
            con = sqlite3.connect("pacman_score.db", isolation_level=None)
            cur = con.cursor()
            cur.execute(f'UPDATE Scoreboard SET total_score = "{self.player_sprite.score}" WHERE player = "{playerId}";')
            con.commit()

        for sprite in self.consumable_list:
            sprite.update()

        if self.buffered_key:
            self.on_key_press(self.buffered_key, key_modifiers=None)

        # closing conditions for the game
        if len(self.consumable_list) == 0 or self.esc_pressed:
            self.close()

            # Implement Database
            playerId = input("Enter your name: ")
            con = sqlite3.connect("pacman_score.db", isolation_level=None)
            cur = con.cursor()
            cur.execute(f'SELECT COUNT(player) FROM Scoreboard;')
            count = cur.fetchone()

            cur.execute(f'UPDATE Scoreboard SET total_score = "{self.player_sprite.score}", player = "{playerId}" WHERE ROWID = "{count}";')
            con.commit()

            cur.execute(f'DROP TABLE IF EXISTS Leaderboard;')
            con.commit()

            cur.execute(f'CREATE TABLE Leaderboard AS SELECT * FROM Scoreboard ORDER BY total_score DESC;')
            con.commit()

        self.ghosts.update()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        # TODO: change the direction pacman is facing based on key press

        # first check if there is a buffered key press before changing the current key press

        if abs(self.player_sprite.center_x - self.tile_center_x) < 4:
            if key == arcade.key.UP and self.next_y_pos in can_move_tiles:
                self.up_pressed = True
                self.down_pressed = False
                self.left_pressed = False
                self.right_pressed = False
                self.update_player_speed()
                self.buffered_key = False
            elif key == arcade.key.DOWN and self.next_y_neg in can_move_tiles:
                self.up_pressed = False
                self.down_pressed = True
                self.left_pressed = False
                self.right_pressed = False
                self.update_player_speed()
                self.buffered_key = False
            else:
                # the next vertical tile isn't a pellet or empty space
                self.buffered_key = key
        if abs(self.player_sprite.center_y - self.tile_center_y) < 4:
            if key == arcade.key.LEFT and self.next_x_neg in can_move_tiles:
                self.up_pressed = False
                self.down_pressed = False
                self.left_pressed = True
                self.right_pressed = False
                self.update_player_speed()
                self.buffered_key = False
            elif key == arcade.key.RIGHT and self.next_x_pos in can_move_tiles:  # height needs to fit through gap
                self.up_pressed = False
                self.down_pressed = False
                self.left_pressed = False
                self.right_pressed = True
                self.update_player_speed()
                self.buffered_key = False
            else:
                # the next horizontal key isn't a pellet or empty space
                self.buffered_key = key

        if key == arcade.key.ESCAPE:
            self.esc_pressed = True

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def update_curr_tile(self) -> (int, int):
        self.curr_row = NUM_ROWS - 1 - int(self.player_sprite.center_y // TILE_SIZE)
        self.curr_col = int(self.player_sprite.center_x // TILE_SIZE)
        self.tile_center_y = int(self.player_sprite.center_y // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2
        self.tile_center_x = self.curr_col * TILE_SIZE + TILE_SIZE // 2



def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen

    # Create and setup the GameView
    game = GameView()
    game.setup()

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()

