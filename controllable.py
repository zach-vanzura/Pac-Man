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
from PIL import Image, ImageOps
import math
from pathlib import Path
from test import TILE_SIZE, MOVEMENT_SPEED, NUM_COLS, NUM_ROWS, SCREEN_WIDTH, SCREEN_HEIGHT
import time
import random

SCATTER_DURATION = 7
CHASE_DURATION = 20

"""
This is the super class for all things controllable in Pac Man: The Player, The Ghosts, **maybe** some walls, 
"""

TEXTURE_ORIENTATIONS = {
    "LEFT_FACING": 3,
    "RIGHT_FACING": 0,
    "UP_FACING": 1,
    "DOWN_FACING": 2
}


class Controllable(arcade.Sprite):
    # TODO: It may be wise to add an is_player boolean but we could also just make the first controllable the player
    def __init__(self, path_to_sprite, tile_size):
        self.txtrs = []
        self.image_ = Image.open(path_to_sprite)
        self.image = self.image_.convert('RGBA')
        # right facing
        self.txtr = arcade.Texture(self.image)
        self.txtrs.append(self.txtr)
        # up facing, rotation is anticlockwise
        self.image_up = self.image.rotate(90)
        self.txtr = arcade.Texture(self.image_up)
        self.txtrs.append(self.txtr)
        #down facing
        self.image_down = self.image_up.rotate(180)
        self.txtr = arcade.Texture(self.image_down)
        self.txtrs.append(self.txtr)
        # start left facing so left txtr is last so it is current at startup
        self.image_left = self.image.rotate(180)
        self.txtr = arcade.Texture(self.image_left)
        self.txtrs.append(self.txtr)

        self.original_size = self.image.width
        self.scale_factor = tile_size / self.original_size
        super().__init__(self.txtr, 1.5 * self.scale_factor, hit_box_algorithm='Simple')
        self.window_width, self.window_height = tile_size * 28, tile_size * 36
        self.is_edible = False
        self.score = 0

    def update(self, delta_time: float = 1 / 60):
        """ Move the Player Sprite """
        # Move player
        # Remove these lines if physics engine is moving player
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x < 0:
            self.texture = self.txtrs[TEXTURE_ORIENTATIONS['LEFT_FACING']]
        elif self.change_x > 0:
            self.texture = self.txtrs[TEXTURE_ORIENTATIONS['RIGHT_FACING']]
        elif self.change_y > 0:
            self.texture = self.txtrs[TEXTURE_ORIENTATIONS['UP_FACING']]
        elif self.change_y < 0:
            self.texture = self.txtrs[TEXTURE_ORIENTATIONS['DOWN_FACING']]
        else:
            # don't change texture if no change in direction
            self.texture = self.texture

        # sprites will wrap around the screen
        if self.left < 0:
            self.right = self.window_width - 1
        elif self.right > self.window_width - 1:
            self.left = 0

        if self.bottom < 0:
            self.top = self.window_height - 1
        elif self.top > self.window_height - 1:
            self.bottom = 0


class Ghost(arcade.Sprite):
    def __init__(self, image_path, ghost_type, player, walls, blinky=None):
        self.image = Image.open(image_path)
        self.original_size = self.image.width
        self.scale_factor = TILE_SIZE / self.original_size
        super().__init__(image_path, 1.5 * self.scale_factor, hit_box_algorithm='Simple')

        self.ghost_type = ghost_type
        self.player = player
        self.walls = walls
        self.blinky = blinky

        self.direction = None
        self.next_direction = None

        # Mode flags
        self.is_chase = False
        self.is_scatter = False
        self.is_frightened = False
        self.is_eaten = False
        self.is_edible = False

        # Scatter corners (tile coordinates)
        self.scatter_targets = {
            "Blinky": (NUM_COLS - 1, 0),
            "Pinky": (0, 0),
            "Inky": (NUM_COLS - 1, NUM_ROWS - 1),
            "Clyde": (0, NUM_ROWS - 1)
        }

        self.set_mode("scatter")
        self.mode_start_time = time.time()
        self.spawn_x = SCREEN_WIDTH // 2
        self.spawn_y = SCREEN_HEIGHT // 2
        self.center_x = self.spawn_x
        self.center_y = self.spawn_y

    def is_aligned_to_tile(self):
        return (self.center_x - TILE_SIZE // 2) % TILE_SIZE == 0 and \
               (self.center_y - TILE_SIZE // 2) % TILE_SIZE == 0

    def can_move_to(self, dx, dy):
        new_x = self.center_x + dx * TILE_SIZE
        new_y = self.center_y + dy * TILE_SIZE
        temp = arcade.Sprite(center_x=new_x, center_y=new_y)
        return not arcade.check_for_collision_with_list(temp, self.walls)

    def set_mode(self, mode):
        self.is_chase = (mode == "chase")
        self.is_scatter = (mode == "scatter")
        self.is_frightened = (mode == "frightened")
        self.is_eaten = (mode == "eaten")
        self.is_edible = (mode == "frightened")
        self.mode_start_time = time.time()

    def update_mode(self):
        elapsed = time.time() - self.mode_start_time
        if self.is_scatter and elapsed > SCATTER_DURATION:
            self.set_mode("chase")
        elif self.is_chase and elapsed > CHASE_DURATION:
            self.set_mode("scatter")

    def get_target_tile(self):
        pacman_tile = (int(self.player.center_x) // TILE_SIZE, int(self.player.center_y) // TILE_SIZE)

        if self.is_scatter:
            return self.scatter_targets[self.ghost_type]

        if self.is_chase:
            if self.ghost_type == "Blinky":
                return pacman_tile
            elif self.ghost_type == "Pinky":
                dx = int(math.copysign(4, self.player.change_x)) if self.player.change_x != 0 else 0
                dy = int(math.copysign(4, self.player.change_y)) if self.player.change_y != 0 else 0
                return (pacman_tile[0] + dx, pacman_tile[1] + dy)
            elif self.ghost_type == "Inky" and self.blinky:
                blinky_tile = (int(self.blinky.center_x) // TILE_SIZE, int(self.blinky.center_y) // TILE_SIZE)
                vector_x = (pacman_tile[0] - blinky_tile[0]) * 2
                vector_y = (pacman_tile[1] - blinky_tile[1]) * 2
                return (blinky_tile[0] + vector_x, blinky_tile[1] + vector_y)
            elif self.ghost_type == "Clyde":
                distance = math.hypot(self.center_x - self.player.center_x, self.center_y - self.player.center_y)
                if distance > TILE_SIZE * 8:
                    return pacman_tile
                else:
                    return self.scatter_targets["Clyde"]

        if self.is_frightened:
            return (random.randint(0, NUM_COLS - 1), random.randint(0, NUM_ROWS - 1))

        if self.is_eaten:
            return (self.spawn_x // TILE_SIZE, self.spawn_y // TILE_SIZE)

        return pacman_tile

    def choose_direction(self):
        if not self.is_aligned_to_tile():
            return

        target = self.get_target_tile()
        x, y = int(self.center_x) // TILE_SIZE, int(self.center_y) // TILE_SIZE

        options = [(0, 1), (0, -1), (-1, 0), (1, 0)]  # up, down, left, right
        best_distance = float("inf")
        best_direction = None

        for dx, dy in options:
            if self.direction and (-dx, -dy) == self.direction:
                continue

            if not self.can_move_to(dx, dy):
                continue

            new_x = x + dx
            new_y = y + dy
            dist = math.hypot(target[0] - new_x, target[1] - new_y)

            if dist < best_distance:
                best_distance = dist
                best_direction = (dx, dy)

        self.next_direction = best_direction

    def update(self, delta_time: float = 1 / 60):
        self.update_mode()
        self.choose_direction()

        if self.is_aligned_to_tile() and self.next_direction:
            self.direction = self.next_direction

        dx = dy = 0
        if self.direction:
            dx, dy = self.direction

        self.change_x = dx * MOVEMENT_SPEED
        self.change_y = dy * MOVEMENT_SPEED

        super().update()

        if self.is_edible and arcade.check_for_collision(self, self.player):
            self.set_mode("eaten")
            self.center_x = self.spawn_x
            self.center_y = self.spawn_y