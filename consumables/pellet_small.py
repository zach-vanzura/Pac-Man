"""
Small pellet class, the class inherits all methods from the Consumable class, allowing to specify scores and
specify typing
"""


from consumable import Consumable
import os


class Pellet(Consumable):
    def __init__(self, tile_size, window_width, window_height):
        self.path_to_sprite = os.path.join('images', 'pellet.png')
        self.original_size = 154
        self.scale_factor = (tile_size / self.original_size) * 0.5
        super().__init__(self.path_to_sprite, self.scale_factor)
        self.score = 10

