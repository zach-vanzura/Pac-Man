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
This is the super class for all things controllable in Pac Man: The Player, The Ghosts, **maybe** some walls, 
"""


class Controllable(arcade.Sprite):
    def __init__(self, window_width, window_height):
        super().__init__()
        self.width, self.height = window_width, window_height

    def update(self, delta_time: float = 1 / 60):
        """ Move the Player Sprite """
        # Move player
        # Remove these lines if physics engine is moving player
        self.center_x += self.change_x
        self.center_y += self.change_y

        # check if out-of-bounds
        # TODO: make it so the player sprite loops around the screen
        # i.e. player moves past the right side of window, pops up at same
        # y coordinate on left side of window
        # similar for top/bottom
        if self.left < 0:
            self.left = 0
        elif self.right > self.width - 1:
            self.right = self.width - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > self.height - 1:
            self.top = self.height - 1