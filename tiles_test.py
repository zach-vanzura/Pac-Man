""" Sprite Sample Program ripped from the Arcade docs"""

import arcade

from consumables.pellet_small import Pellet
from consumables.pellet_energizer import EnergizerPellet as Energizer
import random
from tile import *

# --- Constants ---
SCREEN_WIDTH = 896
SCREEN_HEIGHT = 1152
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
    "=.L|L|.L|||L.LL.L|||L.L||L.=",
    "=o..||.......##.......||..o=",
    "H|L.||.LL.L||||||L.LL.||.L|H",
    "H|L.LL.||.L||LL||L.||.LL.L|H",
    "=......||....||....||......=",
    "=.L||||LL||L.||.L||LL||||L.=",
    "=..........................=",
    "C==========================C",
    "############################",
    "############################"
]

tile_orientations = [
    "############################",
    "############################",
    "############################",
    "y============0y============0",
    "T............TT............T",
    "T.y000.y0000.TT.y0000.y000.T",
    "ToT##T.T###T.TT.T###T.T##ToT",
    "T.z00x.z000x.zx.z000x.z00x.T",
    "T..........................T",
    "T.y000.y0.y0000000.y0.y000.T",
    "T.z00x.TT.z000y00x.TT.z00x.T",
    "T......TT....TT....TT......T",
    "zxxxx0.Tz000#TT#y00xT.yxxxxx",
    "#####T.Ty00x#zx#zTT0T.T#####",
    "#####T.TT##########TT.T#####",
    "#####T.TT#y0000000#TT.T#####",
    "00000x.zx#T######T#zx.z00000",
    "######.###T######T###.######",
    "xxxxx0.y0#T######T#y0.yxxxxx",
    "#####T.TT#z000000x#TT.T#####",
    "#####T.TT##########TT.T#####",
    "#####T.TT#y0000000#TT.T#####",
    "y0000x.zx#z000y00x#zx.z00000",
    "T............TT............T",
    "T.y000.y0000.TT.y0000.y000.T",
    "T.z00T.z000x.zy.z000y.Ty0x.T",
    "To..TT.......##.......TT..oT",
    "z00.TT.y0.y0000000.y0.TT.y0x",
    "y0x.zx.TT.z000y00x.TT.zx.z00",
    "T......TT....TT....TT......T",
    "T.y0000xz000.TT.y00xz00000.T",
    "T.z00000000x.zx.z00000000x.T",
    "T..........................T",
    "z==========================x",
    "############################",
    "############################"
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
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite list
        self.tile_list = arcade.SpriteList()

        # Set up the first tile
        # go through the two lists to get each tile texture and orientation
        y_pos = TILE_SIZE / 2
        for row in (range(len(tile_textures))):  # iterate over y-axis
            x_pos = TILE_SIZE / 2
            for col in (range(len(tile_textures[0]))):  # iterate over x-axis
                # is pellet
                if tile_textures[row][col] == Symbols.PELLET.value:
                    self.tile_sprite = Pellet(TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
                    self.tile_list.append(self.tile_sprite)
                    x_pos += TILE_SIZE
                # is energizer
                elif tile_textures[row][col] == Symbols.ENERGIZER.value:
                    self.tile_sprite = Energizer(TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
                    pass
                # is empty space
                elif tile_textures[row][col] == Symbols.EMPTY_SPACE.value:
                    # increment x, y but do nothing
                    pass
            y_pos += TILE_SIZE

                center_x, center_y = TILE_SIZE // 2
                x_pos, y_pos = center_x + TILE_SIZE, center_y + TILE_SIZE
                tile = Tile(x_pos, y_pos, self.tile_textures[row][col], self.tile_orientations[row][col])
                self.wall_list.append(tile)

    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.tile_list.draw()
        self.tile_list.draw_hit_boxes()


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