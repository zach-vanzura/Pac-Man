"""
Energizer pellet class, the class inherits all methods from the Consumable class, allowing to specify scores and
specify typing
"""

from consumables.pellet_small import Pellet
import os


# TODO: There may need to be more functionality in here based on interactions with pac-man and the ghosts
class EnergizerPellet(Pellet):
    def __init__(self, tile_size, window_width, window_height):
        super().__init__(2 * tile_size, window_width, window_height)
        self.score = 50

