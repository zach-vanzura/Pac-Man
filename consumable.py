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

"""
This is the super class for all things consumable in Pac Man: The Player and the Ghosts (technically), 
Main this class focuses on the pellets, the energizers (the big pellets) and the fruit"""


class Consumable(arcade.Sprite):
    def __init__(self, path_to_sprite, scale, window_width, window_height, ):
        super().__init__(path_to_sprite, scale=scale)
        self.center_x = window_width / 2
        self.center_y = window_height / 2
        self.window_width, self.window_height = window_width, window_height
        self.is_edible = True
        self.is_eaten = False
        self.score = None

    def update(self, delta_time: float = 1 / 60):
        """ Move the Player Sprite """
        # remove pellet if sprite is eaten
        if self.is_eaten:
            self.kill()

    def set_eaten(self):
        self.is_eaten = True