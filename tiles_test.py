""" Sprite Sample Program ripped from the Arcade docs"""

import arcade

from consumables.pellet_small import Pellet
from consumables.pellet_energizer import EnergizerPellet as Energizer
import random
from tile import *

# --- Constants ---
SCREEN_WIDTH = 672
SCREEN_HEIGHT = 864
TILE_SIZE = SCREEN_WIDTH / 28  # 28 is the num tiles per width, size should be square so could also use height / 36

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

class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")

        # Variables that will hold sprite lists
        self.tile_list = None

        # Set up the player info
        self.tile_sprite = None

        # Don't show the mouse cursor
        self.set_mouse_visible(True)

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite list
        self.tile_list = arcade.SpriteList()

        # Set up the first tile
        # go through the two lists to get each tile texture and orientation
        center_y = SCREEN_HEIGHT - TILE_SIZE // 2
        for row in (range(len(tile_textures))):  # iterate over y-axis
            center_x = TILE_SIZE // 2  # reset x pos
            for col in (range(len(tile_textures[0]))):  # iterate over x-axis
                # is pellet
                if tile_textures[row][col] == Symbols.PELLET.value:
                    self.tile_sprite = Pellet(TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
                    self.tile_sprite.center_x, self.tile_sprite.center_y = center_x, center_y
                    self.tile_list.append(self.tile_sprite)
                    center_x += TILE_SIZE
                # is energizer
                elif tile_textures[row][col] == Symbols.ENERGIZER.value:
                    self.tile_sprite = Energizer(TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
                    self.tile_sprite.center_x, self.tile_sprite.center_y = center_x, center_y
                    self.tile_list.append(self.tile_sprite)
                    center_x += TILE_SIZE
                # is empty space
                elif tile_textures[row][col] == Symbols.EMPTY_SPACE.value:
                    center_x += TILE_SIZE
                    continue  # I think this is bad practice but...
                else:
                    texture = tile_textures[row][col]
                    orientation = tile_orientations[row][col]
                    self.tile_sprite = Tile(TILE_SIZE, center_x, center_y, texture, orientation)
                    self.tile_list.append(self.tile_sprite)
                    center_x += TILE_SIZE
            center_y -= TILE_SIZE  # increment y position at each level



    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.tile_list.draw()
        self.tile_list.draw_hit_boxes(color=arcade.color.RED, line_thickness=2)


    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.tile_list.update()


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()