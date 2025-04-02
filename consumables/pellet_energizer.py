"""
Energizer pellet class, the class inherits all methods from the Consumable class, allowing to specify scores and
specify typing
"""

from consumable import Consumable


# TODO: There may need to be more functionality in here based on interactions with pac-man and the ghosts
class EnergizerPellet(Consumable):
    def __init__(self, path_to_sprite, scale):
        super().__init__(path_to_sprite, scale * 2)
        self.score = 50

