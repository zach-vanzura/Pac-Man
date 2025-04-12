"""
Small pellet class, the class inherits all methods from the Consumable class, allowing to specify scores and
specify typing
"""


from consumable import Consumable


class Orange(Consumable):
    def __init__(self, path_to_sprite, scale):
        super().__init__(path_to_sprite, scale)
        self.score = 500

