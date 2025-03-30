# TODO: Begin using pylint

import arcade
from consumables.apple import Apple
from consumables.bell import Bell
from controllable import Controllable
from consumables.cherry import Cherry
from consumables.galaxian import Galaxian
from consumables.pellet_energizer import EnergizerPellet as Energizer
# from consumables.key import Key
from consumables.melon import Melon
from consumables.orange import Orange
from consumables.pellet_small import Pellet
from consumables.strawberry import Strawberry

"""
CS3050: Software Engineering
Final Project -> Pac-Man inspired game

Group Members:
    Lila Mcguirk
    Ashton Putnam
    Zach Vanzura
    Alexa Witkin
"""

"""
Based on Starting Template Using Window Class in the PyArcade Docs
Additionally, added components from Better Move By Keyboard

https://api.arcade.academy/en/latest/example_code/starting_template.html#starting-template
https://api.arcade.academy/en/latest/example_code/sprite_move_keyboard_better.html#sprite-move-keyboard-better

Got the Pac-Man sprite from:
https://www.stickpng.com/img/games/pac-man/pac-man-plain-yellow


- Ashton
"""

"""
Pac-Man and other arcade games use a 5:4 window ratio
pixel width = pixel height * 1.25
for now, 900px = 720px * 1.25
"""

# TODO: create mazes, create start menu screen, add animations, add enemy sprites,
# add pellets, add fruit, add power-ups, add score tracking, add high-score tracking,
# add enemy movement and attacking, add settings menu, add alternative sprites (Jason's face),
# add various menus/start screens/end screens (look up what is actually in pacman),
# etc...


# TODO: assign scaling to each sprite
# Set scale of sprite
SPRITE_SCALING = 0.025
#SPRITE_SCALING = 0.013

# Set tile size
TILE_SIZE = 20

# Set window height and width in 5:4 ratio
WINDOW_WIDTH = 28 * TILE_SIZE  # 28 columns

# Set window title
WINDOW_TITLE = "PAC-MAN"

# Set player movement speed
MOVEMENT_SPEED = 5

# Set fruit point values
KEY_VALUE = 5000


class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        """ Initializer """

        # Call the parent class initializer
        super().__init__()

        # Variables that will hold sprite lists
        self.controllable_list = None
        self.consumable_list = None
        self.to_be_eaten = None

        # Set up the player info
        self.player_sprite = None
        self.pellet_sprite = None
        self.energizer_pellet_sprite = None
        self.cherry_sprite = None
        self.strawberry_sprite = None
        self.orange_sprite = None
        self.apple_sprite = None
        self.melon_sprite = None
        self.galaxian_sprite = None
        self.bell_sprite = None
        # self.key_sprite = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        # fixme: pressing the esc key doesn't close the window yet
        self.esc_pressed = False

        # Set background color
        self.background_color = arcade.color.BLACK

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        self.controllable_list = arcade.SpriteList()
        self.consumable_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        self.wall_map = [
            "############################",
            "############################",
            "############################",
            "C============PP============4",
            "S............||............S",
            "S.*--+.*---+.##.*---+.*--+.S",
            "So/##?./###?.##./###?./##?oS",
            "S.&(().&((().##.&((().&(().S",
            "S..........................S",
            "S.L||L.LL.L||||||L.LL.L||L.S",
            "S.L||L.||.L||LL||L.||.L||L.S",
            "S......||....||....||......S",
            "2====4.|L||L#||#L||L|.C====3",
            "#####S.|L||L#LL#L||L|.S#####",
            "#####S.||##########||.S#####",
            "#####S.||#j==__==j#||.S#####",
            "=====3.LL#=######=#LL.2=====",
            "######.###=######=###.######",
            "=====4.LL#=######=#LL.C=====",
            "#####S.||#j======j#||.S#####",
            "#####S.||##########||.S#####",
            "#####S.||#L||||||L#||.S#####",
            "C====3.LL#L||LL||L#LL.2====4",
            "S............||............S",
            "S.L||L.L|||L.||.L|||L.L||L.S",
            "S.L|L|.L|||L.LL.L|||L.L||L.S",
            "So..||.......##.......||..oS",
            "H|L.||.LL.L||||||L.LL.||.L|H",
            "H|L.LL.||.L||LL||L.||.LL.L|H",
            "S......||....||....||......S",
            "S.L||||LL||L.||.L||LL||||L.S",
            "S..........................S",
            "2==========================3",
            "############################",
            "############################",
        ]

        # Set window height dynamically based on the map
        self.map_height = len(self.wall_map)
        self.window.set_size(WINDOW_WIDTH, self.map_height * TILE_SIZE)

        # Map of characters to wall textures
        tile_textures = {
            "C": arcade.load_texture("images/corner.png"),
            "=": arcade.load_texture("images/straight-piece.png"),
            "S": arcade.load_texture("images/vertical-piece.png"),
            "L": arcade.load_texture("images/single-line-corner.png"),
            "*": arcade.load_texture("images/single-line-corner.png"),
            "-": arcade.load_texture("images/straight-single-line.png"),
            "/": arcade.load_texture("images/vertical-single-line.png"),
            "?": arcade.load_texture("images/vertical-right-single-line.png"),
            "+": arcade.load_texture("images/corner-single-right.png"),
            "(": arcade.load_texture("images/bottom-single-line.png"),
            ")": arcade.load_texture("images/bottom-right-single-corner.png"),
            "&": arcade.load_texture("images/bottom-left-corner-single.png"),
            "1": arcade.load_texture("images/corner.png"),
            "2": arcade.load_texture("images/corner.png"),
            "3": arcade.load_texture("images/corner.png"),
            "4": arcade.load_texture("images/corner.png"),
            "5": arcade.load_texture("images/single-line-corner.png"),
            "6": arcade.load_texture("images/single-line-corner.png"),
            "7": arcade.load_texture("images/single-line-corner.png"),
            "8": arcade.load_texture("images/single-line-corner.png"),

        }

        offset_x = TILE_SIZE // 2
        offset_y = TILE_SIZE // 2
        map_height = self.map_height

        # Build wall tiles using same logic as pellets
        for row_index, row in enumerate(self.wall_map):
            for col_index, tile in enumerate(row):
                x = col_index * TILE_SIZE + offset_x
                y = (map_height - row_index - 1) * TILE_SIZE + offset_y

                if tile in tile_textures:
                    sprite = arcade.Sprite()
                    sprite.texture = tile_textures[tile]
                    sprite.center_x = x
                    sprite.center_y = y

                    # corner pieces (double line)
                    if tile == "1":
                        sprite.angle = 0
                    elif tile == "2":
                        sprite.angle = -90
                    elif tile == "3":
                        sprite.angle = 180
                    elif tile == "4":
                        sprite.angle = 90

                    # corner pieces (single line)
                    if tile == "5":
                        sprite.angle = 0
                    elif tile == "6":
                        sprite.angle = -90
                    elif tile == "7":
                        sprite.angle = 180
                    elif tile == "8":
                        sprite.angle = 90

                    self.wall_list.append(sprite)

                elif tile == ".":
                    self.pellet_sprite = Pellet("images/pellet.png", 0.05, self.window.width, self.window.height)
                    self.pellet_sprite.center_x = x
                    self.pellet_sprite.center_y = y
                    self.consumable_list.append(self.pellet_sprite)

        # Set up Pac-Man
        self.player_sprite = Controllable("images/pacman-static.png",
                                          SPRITE_SCALING, self.window.width, self.window.height)
        # self.player_sprite.center_x = 15
        # self.player_sprite.center_y = 700
        # self.controllable_list.append(self.player_sprite)
        #
        # # Pellet Map
        # # - # is where you don't want pellet to be
        # # - . is where you want pellet to be
        # pellet_map = [
        #     "####...-...g..#.........",
        #     "####.###.####.#.####.##.",
        #     "####.###.####.#.####.##.",
        #     "####............m.......",
        #     "####.###............###.",
        #     "####.............-......",
        #     "########.#..o.......####",
        #     "########.#..........####",
        #     "########.#..........####",
        #     "########.#..-.......####",
        #     "########.#.######.#.####",
        #     "####.....s..............",
        #     "####.###................",
        #     "####.###............c...",
        #     "####.###...-..#....k....",
        #     "####.###......#.........",
        #     "####..b.......#...a.....",
        #     "########################",
        # ]

        #
        # offset_x = TILE_SIZE // 2
        # offset_y = TILE_SIZE // 2
        #
        # for row_index, row in enumerate(pellet_map):
        #     for col_index, tile in enumerate(row):
        #         x = col_index * TILE_SIZE + offset_x
        #         y = (len(pellet_map) - row_index - 1) * TILE_SIZE + offset_y
        #
        #         # small pellet
        #         if tile == ".":
        #             self.pellet_sprite = Pellet("images/pellet.png", 0.05, WINDOW_WIDTH, WINDOW_HEIGHT)
        #             self.pellet_sprite.center_x = x
        #             self.pellet_sprite.center_y = y
        #             self.consumable_list.append(self.pellet_sprite)
        #
        #         # energizer
        #         if tile == "-":
        #             self.energizer_pellet_sprite = Energizer("images/pellet.png", 0.1, WINDOW_WIDTH, WINDOW_HEIGHT)
        #             self.energizer_pellet_sprite.center_x = x
        #             self.energizer_pellet_sprite.center_y = y
        #             self.consumable_list.append(self.energizer_pellet_sprite)
        #
        #         # cherry
        #         if tile == "c":
        #             self.cherry_sprite = Cherry("images/cherry.png", 0.07, WINDOW_WIDTH, WINDOW_HEIGHT)
        #             self.cherry_sprite.center_x = x
        #             self.cherry_sprite.center_y = y
        #             self.consumable_list.append(self.cherry_sprite)
        #
        #         # strawberry
        #         if tile == "s":
        #             self.strawberry_sprite = Strawberry("images/strawberry.png", 0.09, WINDOW_WIDTH, WINDOW_HEIGHT)
        #             self.strawberry_sprite.center_x = x
        #             self.strawberry_sprite.center_y = y
        #             self.consumable_list.append(self.strawberry_sprite)
        #
        #         # orange
        #         if tile == "o":
        #             self.orange_sprite = Orange("images/orange.png", 0.07, WINDOW_WIDTH, WINDOW_HEIGHT)
        #             self.orange_sprite.center_x = x
        #             self.orange_sprite.center_y = y
        #             self.consumable_list.append(self.orange_sprite)
        #
        #         # apple
        #         if tile == "a":
        #             self.apple_sprite = Apple("images/apple.png", 0.1, WINDOW_WIDTH, WINDOW_HEIGHT)
        #             self.apple_sprite.center_x = x
        #             self.apple_sprite.center_y = y
        #             self.consumable_list.append(self.apple_sprite)
        #
        #         # melon
        #         if tile == "m":
        #             self.melon_sprite = Melon("images/melon.png", 0.1, WINDOW_WIDTH, WINDOW_HEIGHT)
        #             self.melon_sprite.center_x = x
        #             self.melon_sprite.center_y = y
        #             self.consumable_list.append(self.melon_sprite)
        #
        #         # galaxian
        #         if tile == "g":
        #             self.galaxian_sprite = Galaxian("images/galaxian.png", 0.1, WINDOW_WIDTH, WINDOW_HEIGHT)
        #             self.galaxian_sprite.center_x = x
        #             self.galaxian_sprite.center_y = y
        #             self.consumable_list.append(self.galaxian_sprite)
        #
        #         # bell
        #         if tile == "b":
        #             self.bell_sprite = Bell("images/bell.png", 0.08, WINDOW_WIDTH, WINDOW_HEIGHT)
        #             self.bell_sprite.center_x = x
        #             self.bell_sprite.center_y = y
        #             self.consumable_list.append(self.bell_sprite)

                # key
                # if tile == "k":
                #     self.key_sprite = Key("images/key.png", 0.08, WINDOW_WIDTH, WINDOW_HEIGHT)
                #     self.key_sprite.center_x = x
                #     self.key_sprite.center_y = y
                #     self.consumable_list.append(self.key_sprite)

    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.controllable_list.draw()
        self.consumable_list.draw()

    def update_player_speed(self):
        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.controllable_list.update(delta_time)
        # find all sprites tha will collide with the pac man
        self.to_be_eaten = self.player_sprite.collides_with_list(self.consumable_list)
        for sprite in self.to_be_eaten:
            sprite.set_eaten()
            self.player_sprite.score += sprite.score

            # elif sprite == self.key_sprite:
            #     self.player_sprite.score += KEY_VALUE
            print(self.player_sprite.score)
        for sprite in self.consumable_list:
            sprite.update()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        # TODO: change the direction pacman is facing based on key press
        if key == arcade.key.UP:
            self.up_pressed = True
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = True
            self.update_player_speed()
        elif key == arcade.key.LEFT:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
            self.update_player_speed()
        elif key == arcade.key.ESCAPE:
            self.esc_pressed = True

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.UP:
            self.up_pressed = False
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = False
            self.update_player_speed()
        elif key == arcade.key.LEFT:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
            self.update_player_speed()
        elif key == arcade.key.ESCAPE:
            self.esc_pressed = False

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, 900, WINDOW_TITLE)

    # Create and setup the GameView
    game = GameView()
    game.setup()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()

