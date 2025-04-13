"""
Small pellet class, the class inherits all methods from the Consumable class, allowing to specify scores and
specify typing
"""


from consumable import Consumable
import os

class Orange(Consumable):
    def __init__(self, scale):
        self.path_to_sprite = os.path.join('images', 'orange.png')
        super().__init__(self.path_to_sprite, scale)
        self.score = 500

