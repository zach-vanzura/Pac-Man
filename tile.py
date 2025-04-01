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

    REFLECT_X = 'x'
    REFLECT_Y = 'y'
    REFLECT_Z = 'z'

    NO_CHANGE = '0'


def orient_image(image: str, operator: str) -> arcade.Texture:
    image = Image.open(image)
    if operator == Orientations.ROTATE.value:
        image = image.rotate(90)
    elif operator == Orientations.REFLECT_X.value:
        image = ImageOps.flip(image)
    elif operator == Orientations.REFLECT_Y.value:
        image = ImageOps.mirror(image)
    elif operator == Orientations.REFLECT_Z.value:
        image = ImageOps.mirror(ImageOps.flip(image))

    # note: the Texture constructor may require a name attribute... the docs online say it does
    # but the docs on python say that it DOES NOT...
    return arcade.Texture(image)


class Tile(arcade.Sprite):
    def __init__(self, center_x, center_y, texture: str, orientation: str):
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

        self.image_path = os.path.join('images', 'tiles', TEXTURES[texture])

        # by checking the orientation, we know how to manipulate the image
        if orientation != Orientations.NO_CHANGE.value:
            name = TEXTURES[texture][0:-4]  # remove the '.png' from the string
            self.image = orient_image(self.image_path, orientation)

        # todo: change scale to be consistent for window
        super().__init__(self.image, 1, center_x, center_y, hit_box_algorithm='Detailed')
