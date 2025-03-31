"""
This is the base tile class that is used to determine the tile texture and the tile orientation for each tile in the
grid.
Each tile in an extension of the sprite arcade class which allows us to determine create walls that pacman can't pass
through
"""

from PIL import Image
import arcade

class Tile(arcade.Sprite):
    def __init__(self, center_x, center_y, texture, orientation):
        # by checking the texture of the spite, we know which image to use
        # if the texture is an empty space (#) or a pellet we can just pass and not add anything,
        # but that can be done in the setup method in the game driver
        if texture == 'INSERT':
            # ADD LOGIC
            pass

        # by checking the orientation, we know how to manipulate the image
        if orientation == 'INSERT':
            # ADD LOGIC
            pass

        # then create the sprite object by calling the super method (probably) using the resulting modified image


