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
import os
from pathlib import Path
from test import TILE_SIZE, GHOST_SPEED, MOVEMENT_SPEED, NUM_COLS, NUM_ROWS, SCREEN_WIDTH, SCREEN_HEIGHT, tile_textures, astar
import time
import random

UPDATES_PER_FRAME = 5

SCATTER_DURATION = 7
CHASE_DURATION = 20
FRIGHTENED_DURATION = 6


TEXTURE_ORIENTATIONS = {
    "LEFT_FACING": 0,
    "RIGHT_FACING": 1,
    "UP_FACING": 2,
    "DOWN_FACING": 3
}


class Controllable(arcade.Sprite):
    def __init__(self, path_to_sprite, tile_size):
        self.cur_texture = 0
        self.cur_direction = 0  # start left facing
        self.default_frames = [
            arcade.load_texture(os.path.join("images", "pacman-animated", "pac-open.png")),
            arcade.load_texture(os.path.join("images", "pacman-animated", "pac-half.png")),
            arcade.load_texture(os.path.join("images", "pacman-animated", "pac-closed.png")),
            arcade.load_texture(os.path.join("images", "pacman-animated", "pac-half.png")),
        ]
        self.txtrs = []
        # default image used for
        self.create_direction_textures()

        self.original_size = Image.open(path_to_sprite).width
        self.scale_factor = tile_size / self.original_size
        super().__init__(self.txtrs[self.cur_direction][self.cur_texture], 1.5 * self.scale_factor, hit_box_algorithm='Simple')
        self.window_width, self.window_height = tile_size * 28, tile_size * 36
        self.is_edible = False
        self.score = 0

        # Movement attributes
        self.direction = None
        self.next_direction = None
        self.change_x = 0
        self.change_y = 0

    def create_direction_textures(self):
        # start left facing
        self.load_directional_animation(rotation=2)
        # right facing, default frames
        self.txtrs.append(self.default_frames)
        # up facing, 270 degree clockwise rotations
        self.load_directional_animation(rotation=3)
        # down facing, 90 degree clockwise
        self.load_directional_animation(rotation=1)

    def load_directional_animation(self, rotation: int):
        """
        rotate each frame based in a certain amount of 90 degree intervals
        """
        tmp_frames = []
        for frame in self.default_frames:
            tmp = frame.rotate_90(rotation)
            tmp_frames.append(tmp)
        self.txtrs.append(tmp_frames)

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
            self.cur_direction = TEXTURE_ORIENTATIONS['LEFT_FACING']

            # TODO: change this to double-index the texture list
        elif self.change_x > 0:
            self.cur_direction = TEXTURE_ORIENTATIONS['RIGHT_FACING']
        elif self.change_y > 0:
            self.cur_direction = TEXTURE_ORIENTATIONS['UP_FACING']
        elif self.change_y < 0:
            self.cur_direction = TEXTURE_ORIENTATIONS['DOWN_FACING']

        # no change in texture if no change in texture
        # TODO: might need an else to continue animation going


        # sprites will wrap around the screen
        if self.left < 0:
            self.right = self.window_width - 1
        elif self.right > self.window_width - 1:
            self.left = 0

        if self.bottom < 0:
            self.top = self.window_height - 1
        elif self.top > self.window_height - 1:
            self.bottom = 0


    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture += 1
        if self.cur_texture > 3 * UPDATES_PER_FRAME:  # eating animation is a sequence of 4 frames
            self.cur_texture = 0

        frame = self.cur_texture // UPDATES_PER_FRAME

        self.texture = self.txtrs[self.cur_direction][frame]




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

        self.previous_mode = None
        self.spawn_point = None
        # Immediately set the default ghost texture to the right‐facing texture.
        self.texture = arcade.load_texture(image_path)
        self.original_texture = self.texture
        self.frightened_texture = arcade.load_texture("images/scared.png")
        self.eaten_texture = arcade.load_texture("images/deadeyes.png")
        self.spawn_waiting_start = None

        self.scatter_targets = {
            "Blinky": (NUM_COLS - 3, NUM_ROWS - 3),
            "Pinky": (2, NUM_ROWS - 3),
            "Inky": (NUM_COLS - 3, 1),
            "Clyde": (2, 1)
        }
        

    def set_mode(self, new_mode):
        old_mode = self.mode  # Capture the current mode before switching

        if new_mode == 'frightened':
            # Record previous mode only if we are coming from a normal state.
            if old_mode not in ('frightened', 'eaten'):
                self.previous_mode = old_mode
            self.mode = 'frightened'
            self.texture = self.frightened_texture
            self.is_edible = True

        elif new_mode == 'eaten':
            # When switching to eaten, if coming from normal mode, record it.
            if old_mode not in ('frightened', 'eaten'):
                self.previous_mode = old_mode
            self.mode = 'eaten'
            self.texture = self.eaten_texture
            self.is_edible = False
            self.spawn_waiting_start = None
            # Clear any movement target so a fresh path to spawn is computed.
            self.target_px = None
            self.current_path = []
            self.path_index = 0

        else:
            # new_mode is either 'scatter' or 'chase'
            self.mode = new_mode
            self.texture = self.original_texture
            self.is_edible = False

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
        
        elif self.mode == 'eaten':
            # Target the spawn room (convert spawn_point in pixel coordinates to tile coordinates)
            if self.spawn_point:
                return (int(self.spawn_point[0] // TILE_SIZE), int(self.spawn_point[1] // TILE_SIZE))

    def update(self, delta_time: float = 1 / 60):
        current_time = time.time()
        elapsed_time = current_time - self.last_mode_switch_time

        # Only perform automatic mode transitions if the ghost is not eaten.
        if self.mode in ('scatter', 'chase', 'frightened'):
            if self.mode == 'scatter' and elapsed_time > SCATTER_DURATION:
                self.set_mode('chase')
            elif self.mode == 'chase' and elapsed_time > CHASE_DURATION:
                self.set_mode('scatter')
            elif self.mode == 'frightened' and elapsed_time > FRIGHTENED_DURATION:
                self.set_mode('scatter')

        # --- Special Handling for Eaten Mode: Head Directly to Spawn ---
        if self.mode == 'eaten' and self.spawn_point is not None:
            # Force the target to be exactly the spawn point (no A*)
            self.target_px = self.spawn_point
            # Compute difference between current position and spawn.
            dx = self.target_px[0] - self.center_x
            dy = self.target_px[1] - self.center_y
            # Use a threshold (e.g., 10 pixels) to consider the ghost “at spawn.”
            threshold = 10
            if abs(dx) < threshold and abs(dy) < threshold:
                # Snap to spawn exactly.
                self.center_x, self.center_y = self.target_px
                if self.spawn_waiting_start is None:
                    # Start waiting; freeze movement.
                    self.spawn_waiting_start = current_time
                    return
                elif current_time - self.spawn_waiting_start < 1:
                    # Still waiting one second.
                    return
                else:
                    # One second has passed – revert mode.
                    self.set_mode(self.previous_mode if self.previous_mode is not None else 'scatter')
                    self.previous_mode = None
                    self.spawn_waiting_start = None
                    # Clear any stale path data so normal pathfinding resumes.
                    self.target_px = None
                    self.current_path = []
                    self.path_index = 0
                    # Do not return—allow normal update processing below.
            else:
                # If not at spawn yet, move directly toward spawn.
                if abs(dx) > abs(dy):
                    self.change_x = GHOST_SPEED if dx > 0 else -GHOST_SPEED
                    self.change_y = 0
                else:
                    self.change_y = GHOST_SPEED if dy > 0 else -GHOST_SPEED
                    self.change_x = 0

                # Move using the computed change values.
                if abs(dx) < GHOST_SPEED:
                    self.center_x = self.target_px[0]
                else:
                    self.center_x += self.change_x

                if abs(dy) < GHOST_SPEED:
                    self.center_y = self.target_px[1]
                else:
                    self.center_y += self.change_y
                return  # Skip normal pathfinding when in eaten mode.

        # --- Normal Movement/Pathfinding for Non-Eaten Modes ---
        curr_tile = (int(self.center_x // TILE_SIZE), int(self.center_y // TILE_SIZE))
        if self.target_px is None or (round(self.center_x), round(self.center_y)) == self.target_px:
            # Only calculate a new path if not in eaten mode.
            if self.mode != 'eaten':
                goal_tile = self.get_target_tile()  # get_target_tile() returns a valid target tile.
                if goal_tile is not None:
                    self.current_path = astar(curr_tile, goal_tile, tile_textures)
                    self.path_index = 0
                else:
                    # Should not happen: safeguard.
                    self.current_path = []
                    self.path_index = 0
            if self.current_path and self.path_index < len(self.current_path):
                next_tile = self.current_path[self.path_index]
                self.path_index += 1
                self.target_px = (
                    next_tile[0] * TILE_SIZE + TILE_SIZE // 2,
                    next_tile[1] * TILE_SIZE + TILE_SIZE // 2
                )

        if self.target_px:
            dx = self.target_px[0] - self.center_x
            dy = self.target_px[1] - self.center_y
            if abs(dx) > abs(dy):
                self.change_x = GHOST_SPEED if dx > 0 else -GHOST_SPEED
                self.change_y = 0
            else:
                self.change_y = GHOST_SPEED if dy > 0 else -GHOST_SPEED
                self.change_x = 0

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

        # if self.mode not in ('frightened', 'eaten'):
        #     if self.change_x < 0:
        #         self.texture = self.txtrs[TEXTURE_ORIENTATIONS['LEFT_FACING']]
        #     elif self.change_x > 0:
        #         self.texture = self.txtrs[TEXTURE_ORIENTATIONS['RIGHT_FACING']]