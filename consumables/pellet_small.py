"""
Small pellet class, the class inherits all methods from the Consumable class, allowing to specify scores and
specify typing
"""


from consumable import Consumable
import os


class Pellet(Consumable):
    def __init__(self, tile_size):
        self.path_to_sprite = os.path.join('images', 'pellet.png')
        super().__init__(self.path_to_sprite, tile_size * 0.5)
        self.score = 10

