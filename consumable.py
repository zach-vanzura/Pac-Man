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

class Consumable(arcade.Sprite):
    """
    This is the super class for all things consumable in Pac-Man:
    The Player and the Ghosts (technically),
    this class focuses on the pellets, the energizers (the big pellets) and the fruit"""
    def __init__(self, path_to_sprite, tile_size):
        self.image = Image.open(path_to_sprite)
        self.original_size = self.image.width
        self.scale_factor = tile_size / self.original_size
        super().__init__(path_to_sprite, self.scale_factor)
        self.is_edible = True
        self.is_eaten = False
        self.score = None

    def update(self, delta_time: float = 1 / 60):
        """ Move the Player Sprite """
        # remove pellet if sprite is eaten
        if self.is_eaten:
            self.kill()

    def set_eaten(self):
        """Sets a boolean to indicate that a consumable has been consumed"""
        self.is_eaten = True
