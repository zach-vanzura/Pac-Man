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
from test import TILE_SIZE, GHOST_SPEED, MOVEMENT_SPEED, NUM_COLS, NUM_ROWS, SCREEN_WIDTH, SCREEN_HEIGHT, tile_textures, astar
import time
import random

SCATTER_DURATION = 7
CHASE_DURATION = 20
FRIGHTENED_DURATION = 6

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

        # Movement attributes
        self.direction = None
        self.next_direction = None
        self.change_x = 0
        self.change_y = 0

    def update(self, delta_time: float = 1 / 60):
        """ Move the Player Sprite """

        if self.direction:
            dx, dy = self.direction
            self.change_x = dx * MOVEMENT_SPEED
            self.change_y = dy * MOVEMENT_SPEED

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

    def is_aligned_to_tile(self):
        return (self.center_x - TILE_SIZE // 2) % TILE_SIZE == 0 and \
               (self.center_y - TILE_SIZE // 2) % TILE_SIZE == 0
    

class Ghost(Controllable):
    def __init__(self, image_path, ghost_type, player, tiles, blinky=None):
        super().__init__(image_path, TILE_SIZE)
        self.ghost_type = ghost_type
        self.player = player
        self.tiles = tiles
        self.blinky = blinky
        self.current_path = []
        self.path_index = 0
        self.target_px = None

        self.mode_timer = 0
        self.mode = 'chase'
        self.last_mode_switch_time = time.time()
        self.scatter_targets = {
            "Blinky": (NUM_COLS - 3, NUM_ROWS - 3),
            "Pinky": (2, NUM_ROWS - 3),
            "Inky": (NUM_COLS - 3, 1),
            "Clyde": (2, 1)
        }
        self.frightened_texture = arcade.load_texture("images/scared.png")
        self.original_texture = self.texture

    def set_mode(self, new_mode):
        """
        Set the ghost's mode (scatter, chase, frightened).
        :param mode: The mode to set (scatter, chase, frightened)
        """
        self.mode = new_mode
        if new_mode in ('scatter', 'chase'):
            self.texture = self.original_texture
            self.is_edible = False
        elif new_mode == 'frightened':
            self.texture = self.frightened_texture
            self.is_edible = True
        # Reset mode timer so the new mode lasts for its full duration
        self.last_mode_switch_time = time.time()

    
    def can_move_to(self, dx, dy):
        """
        Check if the ghost can move to the tile in the given direction.
        :param dx: Change in x direction (e.g., -1, 0, 1)
        :param dy: Change in y direction (e.g., -1, 0, 1)
        :return: True if the ghost can move to the tile, False otherwise
        """
        # Calculate the new position
        new_x = self.center_x + dx * TILE_SIZE
        new_y = self.center_y + dy * TILE_SIZE

        # Check for collisions with walls
        for tile in self.tiles:
            if tile.collides_with_point((new_x, new_y)):
                return False

        return True

    def get_target_tile(self):
        pacman_tile = (self.player.center_x // TILE_SIZE, self.player.center_y // TILE_SIZE)
        
        if self.mode == 'frightened':
            # Randomly choose a tile in the maze
            return (random.randint(0, NUM_COLS - 1), random.randint(0, NUM_ROWS - 1))
        
        elif self.mode == 'scatter':
            # Return the scatter target for this ghost
            return self.scatter_targets[self.ghost_type]
        
        elif self.mode == 'chase':
            if self.ghost_type == "Blinky":
                    return pacman_tile
            
            elif self.ghost_type == "Pinky":
                offset_x = math.cos(math.radians(self.player.angle)) * 4
                offset_y = math.sin(math.radians(self.player.angle)) * 4
                return (pacman_tile[0] + offset_x, pacman_tile[1] + offset_y)
            
            elif self.ghost_type == "Inky" and self.blinky:
                    blinky_tile = (self.blinky.center_x // TILE_SIZE, self.blinky.center_y // TILE_SIZE)
                    vector_x = (pacman_tile[0] - blinky_tile[0]) * 2
                    vector_y = (pacman_tile[1] - blinky_tile[1]) * 2
                    return (blinky_tile[0] + vector_x, blinky_tile[1] + vector_y)
            
            elif self.ghost_type == "Clyde":
                distance = math.hypot(self.center_x - self.player.center_x, self.center_y - self.player.center_y)
                return pacman_tile if distance > TILE_SIZE * 8 else (5, 5)
        
            return pacman_tile

    def update(self, delta_time: float = 1 / 60):
        current_time = time.time()
        elapsed_time = current_time - self.last_mode_switch_time

        if self.mode == 'scatter' and elapsed_time > SCATTER_DURATION:
            self.set_mode('chase')
        elif self.mode == 'chase' and elapsed_time > CHASE_DURATION:
            self.set_mode('scatter')
        elif self.mode == 'frightened' and elapsed_time > FRIGHTENED_DURATION:
            self.set_mode('scatter')

        # Convert pixel -> tile coordinates
        curr_tile = (int(self.center_x // TILE_SIZE), int(self.center_y // TILE_SIZE))

        if self.target_px is None or (round(self.center_x), round(self.center_y)) == self.target_px:
            # We've reached the current target tile; compute next step
            if not self.current_path or self.path_index >= len(self.current_path):
                goal_tile = self.get_target_tile()
                self.current_path = astar(curr_tile, goal_tile, tile_textures)
                self.path_index = 0

            if self.current_path and self.path_index < len(self.current_path):
                next_tile = self.current_path[self.path_index]
                self.path_index += 1
                # Convert tile -> pixel
                self.target_px = (
                    next_tile[0] * TILE_SIZE + TILE_SIZE // 2,
                    next_tile[1] * TILE_SIZE + TILE_SIZE // 2
                )

        if self.target_px:
            dx = self.target_px[0] - self.center_x
            dy = self.target_px[1] - self.center_y

            # Normalize direction
            if abs(dx) > abs(dy):
                self.change_x = GHOST_SPEED if dx > 0 else -GHOST_SPEED
                self.change_y = 0
            else:
                self.change_y = GHOST_SPEED if dy > 0 else -GHOST_SPEED
                self.change_x = 0

            # Prevent overshooting the tile
            if abs(dx) < GHOST_SPEED:
                self.center_x = self.target_px[0]
                self.change_x = 0
            else:
                self.center_x += self.change_x

            if abs(dy) < GHOST_SPEED:
                self.center_y = self.target_px[1]
                self.change_y = 0
            else:
                self.center_y += self.change_y

        # Update texture orientation
        if self.mode != 'frightened':
            if self.change_x < 0:
                self.texture = self.txtrs[TEXTURE_ORIENTATIONS['LEFT_FACING']]
            elif self.change_x > 0:
                self.texture = self.txtrs[TEXTURE_ORIENTATIONS['RIGHT_FACING']]
            #elif self.change_y > 0:
                #self.texture = self.txtrs[TEXTURE_ORIENTATIONS['UP_FACING']]
            #elif self.change_y < 0:
                #self.texture = self.txtrs[TEXTURE_ORIENTATIONS['DOWN_FACING']]
