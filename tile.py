"""
This is the base tile class that is used to determine the tile texture and the tile orientation for each tile in the
grid.
Each tile in an extension of the sprite arcade class which allows us to determine create walls that pacman can't pass
through
"""

import arcade
from enum import Enum
from PIL import Image, ImageOps
import os

TEXTURES = {
    '|': 'single_wall.png',
    '=': 'double_wall.png',
    '_': 'ghost_gate.png',

    'L': 'single_elbow.png',
    'j': 'ghost_cage_elbow.png',
    'C': 'double_elbow.png',

    'P': 'elbow_horizontal_wall.png',
    'H': 'elbow_vertical_wall.png'
}


class Orientations(Enum):
    ROTATE = 'T'
    ROTATE_AND_FLIP = 'Y'

    REFLECT_X = 'x'
    REFLECT_Y = 'y'
    REFLECT_Z = 'z'

    NO_CHANGE = '0'


def orient_image(image: str, operator: str) -> str:
    test_path = image[:-4] + '_' + operator + '.png'  # remove '.png', add the orientation operator and re-add '.png'
    if os.path.exists(test_path):  # remove the'.png' from the textures string
        return test_path

    im = Image.open(image)
    image_transformed = None
    if operator == Orientations.ROTATE.value:
        image_transformed = im.rotate(270)
    elif operator == Orientations.ROTATE_AND_FLIP.value:
        image_transformed_ = im.rotate(90)
        image_transformed = ImageOps.flip(image_transformed_)
    elif operator == Orientations.REFLECT_X.value:
        image_transformed = ImageOps.flip(im)
    elif operator == Orientations.REFLECT_Y.value:
        image_transformed = ImageOps.mirror(im)
    elif operator == Orientations.REFLECT_Z.value:
        image_transformed = im.rotate(180)

    # save the image to be used for later and then return the transformed texture
    to_save = image_transformed
    to_save.save(test_path)

    return test_path


class Tile(arcade.Sprite):
    def __init__(self, tile_size, center_x, center_y, texture: str, orientation: str):
        """
        creates a tile object that extends the sprite class in arcade. This class is used to simplify the maze-making
        process by dissecting the maze into evenly sized tiles. There are ~8 unique tile types in the classic pac man
        maze which allows for a lot of abstraction in the creation process but requires specification of each tile's
        orientation.
        :param center_x: the center x position of the tile
        :param center_y: the center y position of the tile
        :param texture: a character that is used to determine which image to use for the sprite created
        :param orientation: a character that is used to determine how to manipulate the image's orientation
        """

        self.image = None
        self.image_path = os.path.join('images', 'tiles', TEXTURES[texture])
        self.original_size = 768  # original scale of the image
        self.scale_factor = tile_size / self.original_size

        # by checking the orientation, we know how to manipulate the image
        if orientation != Orientations.NO_CHANGE.value:
            self.image = orient_image(self.image_path, orientation)
        else:
            self.image = self.image_path

        super().__init__(self.image, self.scale_factor, center_x, center_y, hit_box_alorithm='Detailed')
