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
from test import TILE_SIZE, GHOST_SPEED, FRIGHTENED_SPEED, MOVEMENT_SPEED, NUM_COLS, NUM_ROWS, SCREEN_WIDTH, SCREEN_HEIGHT, tile_textures, astar, can_move_tiles
import time
import random

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

WAVE_SCHEDULE = [
    ("scatter", 7),
    ("chase", 20),
    ("scatter", 7),
    ("chase", 20),
    ("scatter", 5),
    ("chase", 20),
    ("scatter", 5),
    ("chase", float("inf"))
]


class Controllable(arcade.Sprite):
    # TODO: It may be wise to add an is_player boolean but we could also just make the first controllable the player
    def __init__(self, path_to_sprite, tile_size):
        self.txtrs = []
        self.image = Image.open(path_to_sprite).convert('RGBA')
        self.create_direction_textures()

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

    def create_direction_textures(self):
        # right facing
        self.txtr = arcade.Texture(self.image)
        self.txtrs.append(self.txtr)
        # up facing, rotation is anticlockwise
        self.image_up = self.image.rotate(90)
        self.txtr = arcade.Texture(self.image_up)
        self.txtrs.append(self.txtr)
        # down facing
        self.image_down = self.image_up.rotate(180)
        self.txtr = arcade.Texture(self.image_down)
        self.txtrs.append(self.txtr)
        # start left facing so left txtr is last so it is current at startup
        self.image_left = self.image.rotate(180)
        self.txtr = arcade.Texture(self.image_left)
        self.txtrs.append(self.txtr)

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

        # Pathfinding variables
        self.current_path = []
        self.path_index = 0
        self.target_px = None

        # Ghost state variables
        self.mode = 'scatter'
        self.previous_mode = None
        self.released = False
        self.blinky_release_timestamp = None
        self.spawn_point = None
        self.spawn_waiting_start = None

        # Textures
        self.original_texture = self.txtrs[TEXTURE_ORIENTATIONS['RIGHT_FACING']]
        self.texture = self.original_texture
        self.frightened_texture = arcade.load_texture("images/scared.png")
        self.eaten_texture = arcade.load_texture("images/deadeyes.png")

        # Scatter mode targets 
        self.scatter_targets = {
            "Blinky": (26, 29),
            "Pinky": (1, 26),
            "Inky": (22, 3),
            "Clyde": (1, 3)
        }

        # Mode switch timing variables
        self.mode_wave_index = 0
        self.global_mode_start_time = time.time()
        self.global_timer_paused_at = None

    def set_mode(self, new_mode):
        if new_mode == 'frightened':
            if self.mode not in ('frightened', 'eaten'):
                self.previous_mode = self.mode
            self.mode = 'frightened'
            self.texture = self.frightened_texture
            self.is_edible = True
            self.global_timer_paused_at = time.time()

        elif new_mode == 'eaten':
            if self.mode not in ('frightened', 'eaten'):
                self.previous_mode = self.mode
            self.mode = 'eaten'
            self.texture = self.eaten_texture
            self.is_edible = False
            self.spawn_waiting_start = None
            self.target_px = None
            self.current_path = []
            self.path_index = 0

        else:
            self.mode = new_mode
            self.texture = self.original_texture
            self.is_edible = False
            self.global_timer_paused_at = None
            self.current_path = []
            self.path_index = 0
            self.target_px = None

        self.last_mode_switch_time = time.time()

    def can_move_to(self, dx, dy):
        new_tile_x = int((self.center_x + dx * TILE_SIZE) // TILE_SIZE)
        new_tile_y = int((self.center_y + dy * TILE_SIZE) // TILE_SIZE)

        if 0 <= new_tile_x < NUM_COLS and 0 <= new_tile_y < NUM_ROWS:
            texture = tile_textures[NUM_ROWS - 1 - new_tile_y][new_tile_x]
            return texture in can_move_tiles or texture == '_'
        return False

    def get_target_tile(self):
        pacman_tile = (self.player.center_x // TILE_SIZE, self.player.center_y // TILE_SIZE)

        if self.mode == 'frightened':
            return (random.randint(0, NUM_COLS - 1), random.randint(0, NUM_ROWS - 1))
        
        elif self.mode == 'scatter':
            return self.scatter_targets[self.ghost_type]
        
        elif self.mode == 'chase':
            if self.ghost_type == "Blinky":
                return pacman_tile
            
            elif self.ghost_type == "Pinky":
                offset = {
                    (1, 0): (4, 0),
                    (-1, 0): (-4, 0),
                    (0, 1): (0, 4),
                    (0, -1): (0, -4)
                }.get(self.player.direction, (0, 0))
                return (pacman_tile[0] + offset[0], pacman_tile[1] + offset[1])
            
            elif self.ghost_type == "Inky" and self.blinky:
                blinky_tile = (self.blinky.center_x // TILE_SIZE, self.blinky.center_y // TILE_SIZE)
                offset = {
                    (1, 0): (2, 0),
                    (-1, 0): (-2, 0),
                    (0, 1): (0, 2),
                    (0, -1): (0, -2)
                }.get(self.player.direction, (0, 0))
                intermediate = (pacman_tile[0] + offset[0], pacman_tile[1] + offset[1])
                vector = (intermediate[0] - blinky_tile[0], intermediate[1] - blinky_tile[1])
                return (blinky_tile[0] + vector[0], blinky_tile[1] + vector[1])
            
            elif self.ghost_type == "Clyde":
                distance = math.hypot(self.center_x - self.player.center_x, self.center_y - self.player.center_y)
                return pacman_tile if distance > TILE_SIZE * 8 else self.scatter_targets["Clyde"]
        
        elif self.mode == 'eaten' and self.spawn_point:
            return (int(self.spawn_point[0] // TILE_SIZE), int(self.spawn_point[1] // TILE_SIZE))

    def update(self, delta_time: float = 1 / 60):
        now = time.time()

        if self.mode in ('scatter', 'chase'):
            if self.global_timer_paused_at:
                self.global_mode_start_time += (now - self.global_timer_paused_at)
                self.global_timer_paused_at = None

            elapsed = now - self.global_mode_start_time
            if self.mode_wave_index < len(WAVE_SCHEDULE):
                _, duration = WAVE_SCHEDULE[self.mode_wave_index]
                if elapsed >= duration:
                    self.mode_wave_index += 1
                    if self.mode_wave_index < len(WAVE_SCHEDULE):
                        new_mode, _ = WAVE_SCHEDULE[self.mode_wave_index]
                        self.set_mode(new_mode)
                        self.global_mode_start_time = now
        
        elif self.mode == 'frightened':
            if now - self.last_mode_switch_time >= FRIGHTENED_DURATION:
                self.set_mode(self.previous_mode if self.previous_mode else 'scatter')

        # Handle release logic
        if not self.released:
            if self.ghost_type == "Blinky":
                self.released = True
            elif self.ghost_type == "Pinky":
                if self.blinky_release_timestamp and now - self.blinky_release_timestamp > 3:
                    self.released = True
                else:
                    return
            elif self.ghost_type == "Inky":
                if self.player.score // 10 >= 30 and self.blinky:
                    self.released = True
                else:
                    return
            elif self.ghost_type == "Clyde":
                if self.player.score // 10 >= 60:
                    self.released = True
                else:
                    return

        # Handle scatter mode and pathfinding
        if self.mode == 'scatter' and (self.target_px is None or (round(self.center_x), round(self.center_y)) == self.target_px):
            scatter_tile = self.scatter_targets[self.ghost_type]
            curr_tile = (int(self.center_x // TILE_SIZE), int(self.center_y // TILE_SIZE))
            self.current_path = astar(curr_tile, scatter_tile, tile_textures)
            self.path_index = 0
            if self.current_path and self.path_index < len(self.current_path):
                next_tile = self.current_path[self.path_index]
                self.path_index += 1
                self.target_px = (
                    next_tile[0] * TILE_SIZE + TILE_SIZE // 2,
                    next_tile[1] * TILE_SIZE + TILE_SIZE // 2
                )

        # Handle eaten mode and returning to spawn
        if self.mode == 'eaten' and self.spawn_point:
            curr_tile = (int(self.center_x // TILE_SIZE), int(self.center_y // TILE_SIZE))
            spawn_tile = (int(self.spawn_point[0] // TILE_SIZE), int(self.spawn_point[1] // TILE_SIZE))
            if self.target_px is None or (round(self.center_x), round(self.center_y)) == self.target_px:
                self.current_path = astar(curr_tile, spawn_tile, tile_textures)
                self.path_index = 0
                if self.current_path:
                    next_tile = self.current_path[self.path_index]
                    self.path_index += 1
                    self.target_px = (
                        next_tile[0] * TILE_SIZE + TILE_SIZE // 2,
                        next_tile[1] * TILE_SIZE + TILE_SIZE // 2
                    )

            dx = self.target_px[0] - self.center_x
            dy = self.target_px[1] - self.center_y
            threshold = 4

            if abs(dx) < threshold and abs(dy) < threshold:
                self.center_x, self.center_y = self.target_px
                if not self.spawn_waiting_start:
                    self.spawn_waiting_start = now
                    return
                elif now - self.spawn_waiting_start < 2:
                    return
                else:
                    self.set_mode(self.previous_mode or 'scatter')
                    self.previous_mode = None
                    self.spawn_waiting_start = None
                    self.target_px = None
                    self.current_path = []
                    self.path_index = 0
            else:
                speed = FRIGHTENED_SPEED if self.mode == 'frightened' else GHOST_SPEED
                if abs(dx) > abs(dy):
                    self.change_x = speed if dx > 0 else -speed
                    self.change_y = 0
                else:
                    self.change_y = speed if dy > 0 else -speed
                    self.change_x = 0

                if abs(dx) < GHOST_SPEED:
                    self.center_x = self.target_px[0]
                else:
                    self.center_x += self.change_x

                if abs(dy) < GHOST_SPEED:
                    self.center_y = self.target_px[1]
                else:
                    self.center_y += self.change_y
                return

        # Regular pathfinding (non-eaten)
        curr_tile = (int(self.center_x // TILE_SIZE), int(self.center_y // TILE_SIZE))
        if self.target_px is None or (round(self.center_x), round(self.center_y)) == self.target_px:
            if self.mode != 'eaten':
                goal_tile = self.get_target_tile()
                if goal_tile:
                    self.current_path = astar(curr_tile, goal_tile, tile_textures)
                    self.path_index = 0
            if self.current_path and self.path_index < len(self.current_path):
                next_tile = self.current_path[self.path_index]
                self.path_index += 1
                self.target_px = (
                    next_tile[0] * TILE_SIZE + TILE_SIZE // 2,
                    next_tile[1] * TILE_SIZE + TILE_SIZE // 2
                )
            else:
                # A* failed or path ended prematurely: pick a nearby tile to avoid freezing
                fallback_tile = (int(self.center_x // TILE_SIZE), int(self.center_y // TILE_SIZE))
                self.target_px = (
                    fallback_tile[0] * TILE_SIZE + TILE_SIZE // 2,
                    fallback_tile[1] * TILE_SIZE + TILE_SIZE // 2
                )

        if self.target_px:
            dx = self.target_px[0] - self.center_x
            dy = self.target_px[1] - self.center_y
            speed = FRIGHTENED_SPEED if self.mode == 'frightened' else GHOST_SPEED
            if abs(dx) > abs(dy):
                self.change_x = speed if dx > 0 else -speed
                self.change_y = 0
            else:
                self.change_y = speed if dy > 0 else -speed
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