"""
CS3050: Software Engineering
Final Project -> Pac-Man inspired game

Group Members:
    Lila Mcguirk
    Ashton Putnam
    Zach Vanzura
    Alexa Witkin
"""

import arcade
from PIL import Image

"""
This is the super class for all things controllable in Pac Man: The Player, The Ghosts, **maybe** some walls, 
"""


class Controllable(arcade.Sprite):
    # TODO: It may be wise to add an is_player boolean but we could also just make the first controllable the player
    def __init__(self, path_to_sprite, tile_size):
        self.image = Image.open(path_to_sprite)
        self.original_size = self.image.width
        self.scale_factor = tile_size / self.original_size
        super().__init__(path_to_sprite, 1.5 * self.scale_factor, hit_box_algorithm='Simple')
        self.window_width, self.window_height = tile_size * 28, tile_size * 36
        self.is_edible = False
        self.score = 0

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
