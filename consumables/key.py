"""
Small pellet class, the class inherits all methods from the Consumable class, allowing to specify scores and
specify typing
"""


from consumable import Consumable
import os

class Key(Consumable):
    def __init__(self, scale):
        self.path_to_sprite = os.path.join('images', 'key.png')
        super().__init__(self.path_to_sprite, scale)
        self.score = 5000
