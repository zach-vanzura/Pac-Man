# Imports
import os.path

from arcade import Text
from arcade.shape_list import create_rectangle_filled, create_rectangle_outline

from controllable import *
from consumables import *
from consumables.cherry import Cherry
from consumables.strawberry import Strawberry
from consumables.orange import Orange
from consumables.apple import Apple
from consumables.melon import Melon
from consumables.galaxian import Galaxian
from consumables.bell import Bell
from consumables.key import Key
from consumables.pellet_energizer import EnergizerPellet as Energizer
from consumables.pellet_small import Pellet
from tile import *
import sqlite3
import heapq


"""
CS3050: Software Engineering
Final Project -> Pac-Man inspired game

Group Members:
    Lila Mcguirk
    Ashton Putnam
    Zach Vanzura
    Alexa Witkin
"""


# Set tile size, window height and width
TILE_SIZE = 20
NUM_ROWS = 36
NUM_COLS = 28
SCREEN_HEIGHT = NUM_ROWS * TILE_SIZE  # 36 rows
SCREEN_WIDTH = NUM_COLS * TILE_SIZE  # 28 columns

# Set window title
WINDOW_TITLE = "PAC-MAN"

# Set player and ghost movement speed
"""
Pacman's max movement speed is ~75.75 pixels per second. With a base tile size of 8 pixels, This comes out to ~9.47 
tiles per second. 

Pacman starts moving at 80 % of his max speed, since we aren't really implementing level progression, 80% of pacman's 
max speed is what we will base his movement off of.
"""

MAX_TILES_PER_SECOND = 9.47 / 60

MOVEMENT_SPEED = 0.8 * MAX_TILES_PER_SECOND * TILE_SIZE
GHOST_SPEED = 0.33 * MAX_TILES_PER_SECOND * TILE_SIZE
FRIGHTENED_SPEED = 0.5

# Define symbols
class Symbols(Enum):
    PELLET = '.'
    ENERGIZER = 'o'
    EMPTY_SPACE = '#'
    CHERRY = 'R'
    STRAWBERRY = 'S'
    ORANGE = 'O'
    APPLE = 'A'
    MELON = 'M'
    GALAXIAN = 'G'
    BELL = 'B'
    KEY = 'K'


PAUSE = 5
LIVES = 5


# Define tile textures
tile_textures = [
    "############################",
    "############################",
    "############################",
    "C============PP============C",
    "=............||............=",
    "=.L||L.L|||L.||.L|||L.L||L.=",
    "=o|##|.|###|.||.|###|.|##|o=",
    "=.L||L.L|||L.LL.L|||L.L||L.=",
    "=..........................=",
    "=.L||L.LL.L||||||L.LL.L||L.=",
    "=.L||L.||.L||LL||L.||.L||L.=",
    "=......||....||....||......=",
    "C====L.|L||L#||#L||L|.L====C",
    "#####=.|L||L#LL#L||L|.=#####",
    "#####=.||##########||.=#####",
    "#####=.||#j==__==j#||.=#####",
    "=====L.LL#=######=#LL.L=====",
    "######.###=######=###.######",
    "=====L.LL#=######=#LL.L=====",
    "#####=.||#j======j#||.=#####",
    "#####=.||##########||.=#####",
    "#####=.||#L||||||L#||.=#####",
    "C====L.LL#L||LL||L#LL.L====C",
    "=............||............=",
    "=.L||L.L|||L.||.L|||L.L||L.=",
    "=.L|L|.L|||L.LL.L|||L.|L|L.=",
    "=o..||.......##.......||..o=",
    "H|L.||.LL.L||||||L.LL.||.L|H",
    "H|L.LL.||.L||LL||L.||.LL.L|H",
    "=......||....||....||......=",
    "=.L||||LL||L.||.L||LL||||L.=",
    "=.L||||||||L.LL.L||||||||L.=",
    "=..........................=",
    "C==========================C",
    "############################",
    "##############+#############",
]

# Define tile orientations
tile_orientations = [
    "############################",
    "############################",
    "############################",
    "y0000000000000y0000000000000",
    "Y............TT............T",
    "Y.y000.y0000.TT.y0000.y000.T",
    "YoT##T.T###T.TT.T###T.T##ToT",
    "Y.z00x.z000x.zx.z000x.z00x.T",
    "Y..........................T",
    "Y.y000.y0.y0000000.y0.y000.T",
    "Y.z00x.TT.z000y00x.TT.z00x.T",
    "Y......TT....TT....TT......T",
    "zxxxx0.Tz000#TT#y00xT.yxxxxx",
    "#####Y.Ty00x#zx#z000T.T#####",
    "#####Y.TT##########TT.T#####",
    "#####Y.TT#yxx00xx0#TT.T#####",
    "00000x.zx#T######Y#zx.z00000",
    "######.###T######Y###.######",
    "xxxxx0.y0#T######Y#y0.yxxxxx",
    "#####Y.TT#z000000x#TT.T#####",
    "#####Y.TT##########TT.T#####",
    "#####Y.TT#y0000000#TT.T#####",
    "y0000x.zx#z000y00x#zx.z00000",
    "Y............TT............T",
    "Y.y000.y0000.TT.y0000.y000.T",
    "Y.z00T.z000x.zx.z000x.Ty0x.T",
    "Yo..TT.......##.......TT..oT",
    "z00.TT.y0.y0000000.y0.TT.y0x",
    "y0x.zx.TT.z000y00x.TT.zx.z00",
    "Y......TT....TT....TT......T",
    "Y.y0000xz000.TT.y00xz00000.T",
    "Y.z00000000x.zx.z00000000x.T",
    "Y..........................T",
    "zxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "############################",
    "############################",
]

# Define the tiles that can be moved through
can_move_tiles = ['o', '.', '#', 'C', 'R', 'S', 'O', 'A', 'M', 'G', 'B', 'K']


# Define heuristic function for A* algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Define A* algorithm for Ghost pathfinding
def astar(start, goal, grid):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            break

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_node = (current[0] + dx, current[1] + dy)
            if 0 <= next_node[0] < NUM_COLS and 0 <= next_node[1] < NUM_ROWS:
                tile = tile_textures[NUM_ROWS - 1 - next_node[1]][next_node[0]]
                if tile not in can_move_tiles and tile != '_':
                    continue
                new_cost = cost_so_far[current] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + heuristic(goal, next_node)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current

    # Reconstruct path
    if goal not in came_from:
        return []

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


# Define a function to check if a tile is within bounds
def in_bounds(row, col):
    """
    :param row: the row of the maze
    :param col: the column of the maze
    :return: the character at the given row, col index if there is one
    """

    if 0 <= row < NUM_ROWS:
        col = col % NUM_COLS  # wrap horizontally
        return tile_textures[row][col]
    return None  # treat vertical OOB as wall


# Main GameView class
# This class is the main application window and handles the game logic
class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        """ Initializer """

        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, 'Pac Man')

        # load in this font
        arcade.load_font("fonts/pixeloid_sans/PixeloidSans-Bold.ttf")
        self.font_name = "PixeloidSans-Bold"

        # music
        self.intro_music = None
        self.music_player = None
        self.game_started = False
        self.background_music = None
        self.background_music_player = None

        # chomp sound when eating pellet
        self.last_chomp_time = 0
        self.chomp_cooldown = 0.16
        self.pellet_chomp_sound = arcade.Sound("sounds/pacman_chomp.wav")
        self.powerup_sound = arcade.Sound("sounds/pacman_eatfruit.wav")
        self.ghost_eaten_sound = arcade.Sound("sounds/pacman_eatghost.wav")
        self.death_sound = arcade.Sound("sounds/pacman_death.wav")

        self.curr_row = None
        self.wall_collisions = None
        self.controllable_list = None
        self.tile_list = None
        self.consumable_list = None
        self.to_be_eaten = None
        self.num_fruit_eaten = 0
        self.high_score = 0

        self.player_sprite = None
        self.tile_sprite = None
        self.consumable_sprite = None
        self.static_sprites = None # used for the eaten fruit and remaining lives

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.buffered_key = False

        # initials
        self.show_initials_screen = False
        self.initials = ""
        self.score_submitted = False

        self.initials_bg = create_rectangle_filled(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            300,
            180,
            arcade.color.BLACK
        )

        self.initials_border = create_rectangle_outline(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            300,
            180,
            arcade.color.YELLOW,
            border_width=4
        )

        self.initials_prompt = Text(
            "WRITE YOUR INITIALS",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
            color=arcade.color.WHITE,
            font_size=16,
            anchor_x="center")

        self.esc_pressed = False

        self.background_color = arcade.color.BLACK

        self.physics_engine = None

        self.first_render = True  # New flag to detect the first render

    # Set up the game
    # Initialize the game state, load resources, and set up the game window
    def setup(self):
        # initialize lists
        self.tile_list = arcade.SpriteList(use_spatial_hash=True)
        self.consumable_list = arcade.SpriteList()
        self.controllable_list = arcade.SpriteList()
        self.to_be_eaten = arcade.SpriteList()
        self.static_sprites = arcade.SpriteList()

        # background music
        self.background_music = arcade.Sound("sounds/pacman_beginning.wav", streaming=True)
        #self.background_music_player = self.background_music.play(loop=True)

        # Initialize the player sprite
        self.player_sprite = Controllable(os.path.join('images', 'pacman-animated', 'pac-open.png'), TILE_SIZE)
        self.player_sprite.center_x = TILE_SIZE * 14  # 14 is the x midpoint in the grid
        self.player_sprite.center_y = TILE_SIZE * 9 + TILE_SIZE // 2
        self.lives = LIVES                         # Starting with 5 lives
        self.death_pause_phase = "start"           # Will be one of: None, "death", "post_reset", or "start"
        self.death_pause_start = time.time()       # Timestamp when the current pause phase began
        self.DEATH_PAUSE_DURATION = PAUSE          # Duration for the death collision pause (in seconds)
        self.POST_RESET_PAUSE_DURATION = PAUSE     # Duration for the pause after resetting positions
        self.player_initial_pos = (self.player_sprite.center_x, self.player_sprite.center_y)
        self.player_sprite.direction = (0, 0)
        self.controllable_list.append(self.player_sprite)

        # initialize the static sprites at the bottom of the menu, the n-th life is the current player
        for i in range(self.lives):
            life = Controllable(os.path.join('images', 'pacman-animated', 'pac-open.png'), TILE_SIZE)
            life.center_x = TILE_SIZE + (2 * i * TILE_SIZE)  # move each static over to the right by two tiles
            life.center_y = TILE_SIZE
            self.static_sprites.append(life)

        # Initialize the Ghosts sprites
        self.blinky = Ghost("images/blinky.png", "Blinky", self.player_sprite, self.tile_list)
        self.pinky = Ghost("images/pinky.png", "Pinky", self.player_sprite, self.tile_list)
        self.inky = Ghost("images/inky.png", "Inky", self.player_sprite, self.tile_list, blinky=self.blinky)
        self.clyde = Ghost("images/clyde.png", "Clyde", self.player_sprite, self.tile_list)

        # Add ghosts to the ghosts list
        self.ghosts = arcade.SpriteList()
        self.ghosts.extend([self.blinky, self.pinky, self.inky, self.clyde])

        # Add ghosts to controllable list
        self.controllable_list.extend(self.ghosts)

        # Ghost spawn room
        spawn_x = TILE_SIZE * 13.5 + TILE_SIZE // 2
        spawn_y = TILE_SIZE * 17.5  # original spawn room row

        # Save the ghost spawn room position
        self.spawn_room_pos = (spawn_x, spawn_y)

        # ghost spawn points
        self.blinky.center_x = TILE_SIZE * 13.5 + TILE_SIZE // 2  # middle of gate
        self.blinky.center_y = TILE_SIZE * 20.5 + TILE_SIZE

        spawn_x = TILE_SIZE * 13.5 + TILE_SIZE // 2
        spawn_y = TILE_SIZE * 17.5  # original spawn room row
        self.inky.center_x = spawn_x - (TILE_SIZE + 15)
        self.inky.center_y = spawn_y + TILE_SIZE
        self.pinky.center_x = spawn_x
        self.pinky.center_y = spawn_y + TILE_SIZE
        self.clyde.center_x = spawn_x + (TILE_SIZE + 15)
        self.clyde.center_y = spawn_y + TILE_SIZE

        # Record the spawn points so ghosts can return here when eaten
        self.blinky.spawn_point = (self.blinky.center_x, self.blinky.center_y)
        self.pinky.spawn_point = (self.pinky.center_x, self.pinky.center_y)
        self.inky.spawn_point = (self.inky.center_x, self.inky.center_y)
        self.clyde.spawn_point = (self.clyde.center_x, self.clyde.center_y)

        self.blinky.set_mode("chase")
        self.blinky_release_timestamp = time.time()
        self.pinky.blinky_release_timestamp = self.blinky_release_timestamp
        self.inky.blinky_release_timestamp = self.blinky_release_timestamp
        self.clyde.blinky_release_timestamp = self.blinky_release_timestamp

        # Physics engines
        # self.player_physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.tile_list)
        # self.ghost_physics_engines = [
        #     arcade.PhysicsEngineSimple(ghost, self.tile_list) for ghost in self.ghosts
        # ]

        # Go through the two lists to get each tile texture and orientation
        center_y = SCREEN_HEIGHT - TILE_SIZE // 2
        for row in (range(len(tile_textures))):  # iterate over y-axis
            center_x = TILE_SIZE // 2  # reset x pos
            for col in (range(len(tile_textures[0]))):  # iterate over x-axis
                # is pellet
                if tile_textures[row][col] == Symbols.PELLET.value:
                    self.consumable_sprite = Pellet(TILE_SIZE)
                    self.consumable_sprite.center_x, self.consumable_sprite.center_y = center_x, center_y
                    self.consumable_list.append(self.consumable_sprite)
                # is energizer
                elif tile_textures[row][col] == Symbols.ENERGIZER.value:
                    self.consumable_sprite = Energizer(TILE_SIZE)
                    self.consumable_sprite.center_x, self.consumable_sprite.center_y = center_x, center_y
                    self.consumable_list.append(self.consumable_sprite)
                # is empty space
                elif tile_textures[row][col] == Symbols.EMPTY_SPACE.value:
                    center_x += TILE_SIZE
                    continue
                else:
                    texture = tile_textures[row][col]

                    if texture == '+':
                        self.logo_sprite = arcade.Sprite("images/pac-man-logo.png", scale=0.1)
                        self.logo_sprite.center_x = center_x
                        self.logo_sprite.center_y = center_y + 10

                        # need hasattr or it won't work - adds it to sprite list
                        if not hasattr(self, "logo_list"):
                            self.logo_list = arcade.SpriteList()

                        self.logo_list.append(self.logo_sprite)

                    else:
                        orientation = tile_orientations[row][col]
                        self.tile_sprite = Tile(TILE_SIZE, center_x, center_y, texture, orientation)
                        self.tile_list.append(self.tile_sprite)

                center_x += TILE_SIZE
            center_y -= TILE_SIZE  # increment y position at each level

        # Implement Database
        player_id = "1" # alter if additional player is added
        con = sqlite3.connect("pacman_score.db", isolation_level=None)
        cur = con.cursor()
        cur.execute(f'INSERT INTO ScoreBoard (total_score,player) VALUES ("{self.player_sprite.score}", "{player_id}");')
        con.commit()

        # Fetch the highest score in the database
        cur.execute("SELECT MAX(total_score) FROM Scoreboard;")
        result = cur.fetchone()
        self.high_score = result[0] if result and result[0] is not None else 0

        # Pause the game for 5 seconds at the start
        self.is_paused = True
        self.pause_timer = PAUSE

    def on_draw(self):

        if self.first_render:
            self.background_music_player = self.background_music.play(loop=True)
            self.death_pause_start = time.time()  # Set the start time for the pause
            self.first_render = False  # Set the flag to False after the first render

        self.clear()
        self.tile_list.draw()
        self.consumable_list.draw()
        # self.tile_list.draw_hit_boxes(color=arcade.color.RED, line_thickness= 1)
        self.controllable_list.draw()
        # self.controllable_list.draw_hit_boxes(color=arcade.color.PINK, line_thickness=1)
        self.ghosts.draw()
        self.logo_list.draw()
        self.static_sprites.draw()

        # function to change the font not working
        score_text = str(self.player_sprite.score)

        # If in the "start" pause phase (e.g., at level launch or immediately after a reset)
        if self.death_pause_phase in ("start", "post_reset"):
            # Use the saved spawn room coordinates
            if hasattr(self, "spawn_room_pos"):
                spawn_x, spawn_y = self.spawn_room_pos
                # Adjust the y value so that the text is drawn directly under the ghost room.
                ready_y = spawn_y - TILE_SIZE // 2
            else:
                # Fallback (center of screen)
                spawn_x = SCREEN_WIDTH // 2
                ready_y = SCREEN_HEIGHT // 2

            arcade.draw_text("READY!",
                            spawn_x,
                            ready_y - 40,
                            arcade.color.YELLOW,
                            16,
                            anchor_x="center")

        arcade.draw_text(score_text,
                         20,
                         SCREEN_HEIGHT - 40,
                         arcade.color.WHITE,
                         14,
                         font_name=self.font_name,
                         anchor_x="left")

        arcade.draw_text("HIGH SCORE",
                         SCREEN_WIDTH // 2,
                         SCREEN_HEIGHT - 30,
                         arcade.color.WHITE,
                         16,
                         anchor_x="center",
                         font_name="PixeloidSans-Bold")

        arcade.draw_text(str(self.high_score),
                         SCREEN_WIDTH // 2,
                         SCREEN_HEIGHT - 50,
                         arcade.color.WHITE,
                         14,
                         anchor_x="center",
                         font_name=self.font_name)

        # window to submit initials
        if self.show_initials_screen:
            # Draw the GAME OVER header above the initials box.
            arcade.draw_text("GAME OVER",
                            SCREEN_WIDTH // 2,
                            SCREEN_HEIGHT // 2 + 100,  # adjust Y offset to position above the prompt box
                            arcade.color.RED,
                            20,
                            anchor_x="center")

            self.initials_bg.draw()
            self.initials_border.draw()

            arcade.draw_text("WRITE YOUR INITIALS",
                             SCREEN_WIDTH // 2,
                             SCREEN_HEIGHT // 2 + 50,
                             arcade.color.WHITE,
                             16,
                             anchor_x="center")

            arcade.draw_text(self.initials or "_ _ _",
                             SCREEN_WIDTH // 2,
                             SCREEN_HEIGHT // 2 + 5,
                             arcade.color.WHITE,
                             28,
                             anchor_x="center")

            arcade.draw_text("Press ENTER to Submit",
                             SCREEN_WIDTH // 2,
                             SCREEN_HEIGHT // 2 - 40,
                             arcade.color.GRAY,
                             12,
                             anchor_x="center")

    def update_player_speed(self):
        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        if self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

        # Save logical direction for ghost AI
        if self.player_sprite.change_x > 0:
            self.player_sprite.direction = (1, 0)
        elif self.player_sprite.change_x < 0:
            self.player_sprite.direction = (-1, 0)
        elif self.player_sprite.change_y > 0:
            self.player_sprite.direction = (0, 1)
        elif self.player_sprite.change_y < 0:
            self.player_sprite.direction = (0, -1)

    def on_update(self, delta_time=60):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """

        # initials
        if self.show_initials_screen:
            return
        
        if self.lives == 0:
            self.show_initials_screen = True
        
        current_time = time.time()
    
        # Handle pause phases
        if self.death_pause_phase is not None:
            if self.death_pause_phase == "start":
                if current_time - self.death_pause_start < PAUSE:
                    # During the start-of-level pause, do nothing (freeze frame)
                    return
                else:
                    # Start-of-level pause is over: resume normal gameplay
                    self.death_pause_phase = None
                    return
            elif self.death_pause_phase == "death":
                if current_time - self.death_pause_start < self.DEATH_PAUSE_DURATION:
                    # During the initial death pause, do nothing (freeze frame)
                    return
                else:
                    # Death pause duration is over: Reset positions and start the post-reset pause
                    self.reset()
                    self.death_pause_phase = "post_reset"
                    self.death_pause_start = current_time
                    return
            elif self.death_pause_phase == "post_reset":
                if current_time - self.death_pause_start < self.POST_RESET_PAUSE_DURATION:
                    # Still in the post-reset pause: do nothing
                    return
                else:
                    # Post-reset pause is finished: resume normal game updates
                    self.death_pause_phase = None
                    # Fall through to normal update processing

        # Update the physics engine
        # self.player_physics_engine.update()
        # for engine in self.ghost_physics_engines:
        #     engine.update()
        
        # position checks before collision checks

        # check the next tile, up, down, left, or right is within bounds
        self.update_curr_tile()
        self.next_y_pos = in_bounds(self.curr_row - 1, self.curr_col)  # going up, decrement index
        self.next_y_neg = in_bounds(self.curr_row + 1, self.curr_col)
        self.next_x_pos = in_bounds(self.curr_row, self.curr_col + 1)
        self.next_x_neg = in_bounds(self.curr_row, self.curr_col - 1)

        if self.up_pressed and self.next_y_pos not in can_move_tiles:
            self.player_sprite.center_y = self.tile_center_y - TILE_SIZE // 4
        if self.down_pressed and self.next_y_neg not in can_move_tiles:
            self.player_sprite.center_y = self.tile_center_y + TILE_SIZE // 4
        if self.left_pressed and self.next_x_neg not in can_move_tiles:
            self.player_sprite.center_x = self.tile_center_x + TILE_SIZE // 4
        if self.right_pressed and self.next_x_pos not in can_move_tiles:  # needed for tunnel
            self.player_sprite.center_x = self.tile_center_x - TILE_SIZE // 4

        #self.physics_engine.update()
        self.controllable_list.update(delta_time)
        self.player_sprite.update_animation()

        # Go through the two lists to get each tile texture and orientation
        center_y = 9 * TILE_SIZE + TILE_SIZE // 2
        center_x = 12 * TILE_SIZE
        elasped_time = current_time - self.death_pause_start
        print(current_time - self.death_pause_start)
        if 10 < elasped_time < 11 and not any(isinstance(c, Cherry) for c in self.consumable_list):
            self.consumable_sprite = Cherry(TILE_SIZE)
            self.consumable_sprite.center_x, self.consumable_sprite.center_y = (TILE_SIZE * 14,
                                                                                TILE_SIZE * 15 + TILE_SIZE // 2)
            self.consumable_list.append(self.consumable_sprite)
        elif 30 < elasped_time < 31 and not any(isinstance(c, Strawberry) for c in self.consumable_list):
            self.consumable_sprite = Strawberry(TILE_SIZE)
            self.consumable_sprite.center_x, self.consumable_sprite.center_y = (TILE_SIZE * 14,
                                                                                TILE_SIZE * 15 + TILE_SIZE // 2)
            self.consumable_list.append(self.consumable_sprite)
        elif 50 < elasped_time < 51 and not any(isinstance(c, Orange) for c in self.consumable_list):
            self.consumable_sprite = Orange(TILE_SIZE)
            self.consumable_sprite.center_x, self.consumable_sprite.center_y = (TILE_SIZE * 14,
                                                                                TILE_SIZE * 15 + TILE_SIZE // 2)
            self.consumable_list.append(self.consumable_sprite)
        elif 70 < elasped_time < 71 and not any(isinstance(c, Apple) for c in self.consumable_list):
            self.consumable_sprite = Apple(TILE_SIZE)
            self.consumable_sprite.center_x, self.consumable_sprite.center_y = (TILE_SIZE * 14,
                                                                                TILE_SIZE * 15 + TILE_SIZE // 2)
            self.consumable_list.append(self.consumable_sprite)
        elif 100 < elasped_time < 101 and not any(isinstance(c, Melon) for c in self.consumable_list):
            self.consumable_sprite = Melon(TILE_SIZE)
            self.consumable_sprite.center_x, self.consumable_sprite.center_y = (TILE_SIZE * 14,
                                                                                TILE_SIZE * 15 + TILE_SIZE // 2)
            self.consumable_list.append(self.consumable_sprite)
        elif 130 < elasped_time < 131 and not any(isinstance(c, Galaxian) for c in self.consumable_list):
            self.consumable_sprite = Galaxian(TILE_SIZE)
            self.consumable_sprite.center_x, self.consumable_sprite.center_y = (TILE_SIZE * 14,
                                                                                TILE_SIZE * 15 + TILE_SIZE // 2)
            self.consumable_list.append(self.consumable_sprite)
        elif 160 < elasped_time < 161 and not any(isinstance(c, Bell) for c in self.consumable_list):
            self.consumable_sprite = Bell(TILE_SIZE)
            self.consumable_sprite.center_x, self.consumable_sprite.center_y = (TILE_SIZE * 14,
                                                                                TILE_SIZE * 15 + TILE_SIZE // 2)
            self.consumable_list.append(self.consumable_sprite)
        elif 200 < elasped_time < 201 and not any(isinstance(c, Key) for c in self.consumable_list):
            self.consumable_sprite = Key(TILE_SIZE)
            self.consumable_sprite.center_x, self.consumable_sprite.center_y = (TILE_SIZE * 14,
                                                                                TILE_SIZE * 15 + TILE_SIZE // 2)
            self.consumable_list.append(self.consumable_sprite)


        # find all sprites that will collide with the pac man
        self.to_be_eaten = self.player_sprite.collides_with_list(self.consumable_list)
        for sprite in self.to_be_eaten:
            # this check isn't really necessary right now, but it may be helpful in the future with ghosts ( it is! )
            if sprite.is_edible:
                sprite.set_eaten()
                self.player_sprite.score += sprite.score
                self.consumable_list.remove(sprite)

                # play chomp noise
                if isinstance(sprite, Pellet):
                    current_time = time.time()
                    if current_time - self.last_chomp_time >= self.chomp_cooldown:
                        self.pellet_chomp_sound.play(speed=1.5)
                        self.last_chomp_time = current_time

                # Enter frightened mode if Energizer pellet
                # also play noise
                if isinstance(sprite, Energizer):
                    self.powerup_sound.play()
                    for ghost in self.ghosts:
                        ghost.set_mode('frightened')

                # sprite eaten is a fruit
                if not (isinstance(sprite, Pellet) or isinstance(sprite, Ghost) or isinstance(sprite, Energizer)):
                    self.powerup_sound.play()
                    sprite.center_x, sprite.center_y = TILE_SIZE * (NUM_COLS - 1 - 2 * self.num_fruit_eaten), TILE_SIZE
                    self.static_sprites.append(sprite)
                    self.num_fruit_eaten += 1

            # print the score
            print(self.player_sprite.score)

            # Implement Database
            player_id = "1"  # alter if additional player is added
            con = sqlite3.connect("pacman_score.db", isolation_level=None)
            cur = con.cursor()
            cur.execute(f'UPDATE Scoreboard SET total_score = "{self.player_sprite.score}" WHERE player = "{player_id}";')
            con.commit()

        # update the consumable sprites
        for sprite in self.consumable_list:
            sprite.update()
        
        # Collision check with ghosts:
        if self.death_pause_phase is None:  # Only process collisions if not in a death pause.
            ghost_hit_list = self.player_sprite.collides_with_list(self.ghosts)
            for ghost in ghost_hit_list:
                if ghost.mode == 'frightened':
                    ghost.set_mode('eaten')
                    ghost.score = 200   # Award points for eating the ghost.
                    self.player_sprite.score += ghost.score
                    # Play ghost eaten sound
                    self.ghost_eaten_sound.play()
                elif ghost.mode in ('chase', 'scatter'):
                    # Collision with an active (non-frightened) ghost: register a death.
                    self.lives -= 1
                    self.static_sprites.pop(0)  # remove the first element, this way we can add the fruit to the end
                    print(f"Lives remaining: {self.lives}")
                    # Start the death pause cycle only if not already active.
                    # play death sound
                    self.death_sound.play()
                    self.death_pause_phase = "death"
                    self.death_pause_start = time.time()
                    # Break out of the collision loop to avoid multiple detections.
                    break

        for ghost in self.ghosts:
            if ghost.released:
                ghost.update()

        if self.buffered_key:
            self.on_key_press(self.buffered_key, key_modifiers=None)

       # Only count pellets and energizers
        remaining_edibles = [s for s in self.consumable_list if isinstance(s, (Pellet, Energizer))]
        if len(remaining_edibles) == 0:
            self.reset_level()

        # quick closing conditions for the game
        # if self.esc_pressed:
            # self.close()
        

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if not self.game_started:
            self.game_started = True
            if self.background_music_player:
                self.background_music_player.pause()
            return

        self.update_curr_tile()

        # first check if there is a buffered key press before changing the current key press
        # once you push enter the whole game should close
        if self.show_initials_screen:
            if key == arcade.key.BACKSPACE and len(self.initials) > 0:
                self.initials = self.initials[:-1]
            elif key == arcade.key.ENTER:
                self.score_submitted = True
                self.show_initials_screen = False
                # Implement Database
                player_id = self.initials
                con = sqlite3.connect("pacman_score.db", isolation_level=None)
                cur = con.cursor()
                cur.execute(f'SELECT COUNT(player) FROM Scoreboard;')
                count = cur.fetchone()

                cur.execute(f'UPDATE Scoreboard SET total_score = "{self.player_sprite.score}", player = "{player_id}" WHERE ROWID = "{count[0]}";')
                con.commit()

                cur.execute(f'DROP TABLE IF EXISTS Leaderboard;')
                con.commit()

                cur.execute(f'CREATE TABLE Leaderboard AS SELECT * FROM Scoreboard ORDER BY total_score DESC;')
                con.commit()
                self.close()
            return

        if key == arcade.key.ESCAPE:
            self.show_initials_screen = True
            return

        if abs(self.player_sprite.center_x - self.tile_center_x) < 4:
            if key == arcade.key.UP and self.next_y_pos in can_move_tiles:
                self.up_pressed = True
                self.down_pressed = False
                self.left_pressed = False
                self.right_pressed = False
                self.update_player_speed()
                self.buffered_key = False
            elif key == arcade.key.DOWN and self.next_y_neg in can_move_tiles:
                self.up_pressed = False
                self.down_pressed = True
                self.left_pressed = False
                self.right_pressed = False
                self.update_player_speed()
                self.buffered_key = False
            else:
                # the next vertical tile isn't a pellet or empty space
                self.buffered_key = key
        if abs(self.player_sprite.center_y - self.tile_center_y) < 4:
            if key == arcade.key.LEFT and self.next_x_neg in can_move_tiles:
                self.up_pressed = False
                self.down_pressed = False
                self.left_pressed = True
                self.right_pressed = False
                self.update_player_speed()
                self.buffered_key = False
            elif key == arcade.key.RIGHT and self.next_x_pos in can_move_tiles:  # height needs to fit through gap
                self.up_pressed = False
                self.down_pressed = False
                self.left_pressed = False
                self.right_pressed = True
                self.update_player_speed()
                self.buffered_key = False
            else:
                # the next horizontal key isn't a pellet or empty space
                self.buffered_key = key


    # method to type initials
    def on_text(self, text):
        if self.show_initials_screen and not self.score_submitted:
            if len(self.initials) < 3 and text.isalpha():
                self.initials += text.upper()

    def reset(self):
        """
        Reset Pac-Man and ghost positions to their starting spawn points.
        Consumables and the current score remain unchanged.
        """
        # Reset Pac-Man's position using a stored initial position.
        self.player_sprite.center_x, self.player_sprite.center_y = self.player_initial_pos
        
        # Reset ghosts: iterate through each ghost and reset their positions and mode.
        for ghost in self.ghosts:
            if ghost.spawn_point is not None:
                ghost.center_x, ghost.center_y = ghost.spawn_point
            # Reset ghost mode to 'chase' (or your default) and clear path data.
            ghost.set_mode('chase')
            ghost.target_px = None
            ghost.current_path = []
            ghost.path_index = 0

    def update_curr_tile(self):
        """
        Update the player's current tile and the adjacent tiles.
        """
        # Calculate the player's current row and column
        self.curr_row = NUM_ROWS - 1 - int(self.player_sprite.center_y // TILE_SIZE)
        self.curr_col = int(self.player_sprite.center_x // TILE_SIZE)

        # Calculate the center of the current tile
        self.tile_center_y = int(self.player_sprite.center_y // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2
        self.tile_center_x = self.curr_col * TILE_SIZE + TILE_SIZE // 2

        # Check the adjacent tiles
        self.next_y_pos = in_bounds(self.curr_row - 1, self.curr_col)  # Tile above
        self.next_y_neg = in_bounds(self.curr_row + 1, self.curr_col)  # Tile below
        self.next_x_pos = in_bounds(self.curr_row, self.curr_col + 1)  # Tile to the right
        self.next_x_neg = in_bounds(self.curr_row, self.curr_col - 1)  # Tile to the left

    def reset_level(self):
        """
        Reset the current level: regenerate all consumable pellets and energizers
        and reset the positions of Pac-Man and ghosts. The score and lives remain unchanged.
        """
        # Clear the current consumables.
        self.consumable_list = arcade.SpriteList()

        # Rebuild the consumables from the maze layout.
        center_y = SCREEN_HEIGHT - TILE_SIZE // 2
        for row in range(len(tile_textures)):  # iterate over y-axis
            center_x = TILE_SIZE // 2  # reset x pos for each row
            for col in range(len(tile_textures[0])):  # iterate over x-axis
                # Check the tile character for pellet or energizer.
                if tile_textures[row][col] == Symbols.PELLET.value:
                    consumable_sprite = Pellet(TILE_SIZE)
                    consumable_sprite.center_x, consumable_sprite.center_y = center_x, center_y
                    self.consumable_list.append(consumable_sprite)
                elif tile_textures[row][col] == Symbols.ENERGIZER.value:
                    consumable_sprite = Energizer(TILE_SIZE)
                    consumable_sprite.center_x, consumable_sprite.center_y = center_x, center_y
                    self.consumable_list.append(consumable_sprite)
                center_x += TILE_SIZE
            center_y -= TILE_SIZE

        # Reset positions for the player and all ghosts.
        self.reset()

        self.death_pause_phase = "start"  # Reset the death pause phase to start
        self.death_pause_start = time.time()


def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen

    # Create and setup the GameView
    game = GameView()
    game.setup()

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()