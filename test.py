# TODO: Begin using pylint

import arcade
from consumables.apple import Apple
from consumables.bell import Bell
from controllable import Controllable
from consumables.cherry import Cherry
from consumables.galaxian import Galaxian
from consumables.pellet_energizer import EnergizerPellet as Energizer
from consumables.key import Key
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

#TODO: create mazes, create start menu screen, add animations, add enemy sprites,
# add pellets, add fruit, add power-ups, add score tracking, add high-score tracking,
# add enemy movement and attacking, add settings menu, add alternative sprites (Jason's face),
# add various menus/start screens/end screens (look up what is actually in pacman),
# etc...


# TODO: assign scaling to each sprite
# Set scale of sprite
SPRITE_SCALING = 0.013

# Set window height and width in 5:4 ratio
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 720

# Set window title
WINDOW_TITLE = "PAC-MAN"

# Set player movement speed
MOVEMENT_SPEED = 5

# Set tile size
TILE_SIZE = 32


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
        self.key_sprite = None

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

        # Set up Pac-Man
        self.player_sprite = Controllable("images/pacman-static.png",
                                          SPRITE_SCALING, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.player_sprite.center_x = 15
        self.player_sprite.center_y = 700
        self.controllable_list.append(self.player_sprite)

        # Pellet Map
        # - # is where you don't want pellet to be
        # - . is where you want pellet to be
        pellet_map = [
            "####...-...g..#.........",
            "####.###.####.#.####.##.",
            "####.###.####.#.####.##.",
            "####............m.......",
            "####.###............###.",
            "####.............-......",
            "########.#..o.......####",
            "########.#..........####",
            "########.#..........####",
            "########.#..-.......####",
            "########.#.######.#.####",
            "####.....s..............",
            "####.###................",
            "####.###............c...",
            "####.###...-..#....k....",
            "####.###......#.........",
            "####..b.......#...a.....",
            "########################",
        ]

        offset_x = TILE_SIZE // 2
        offset_y = TILE_SIZE // 2

        for row_index, row in enumerate(pellet_map):
            for col_index, tile in enumerate(row):
                x = col_index * TILE_SIZE + offset_x
                y = (len(pellet_map) - row_index - 1) * TILE_SIZE + offset_y

                # small pellet
                if tile == ".":
                    self.pellet_sprite = Pellet("images/pellet.png", 0.05, WINDOW_WIDTH, WINDOW_HEIGHT)
                    self.pellet_sprite.center_x = x
                    self.pellet_sprite.center_y = y
                    self.consumable_list.append(self.pellet_sprite)

                # energizer
                if tile == "-":
                    self.energizer_pellet_sprite = Energizer("images/pellet.png", 0.1, WINDOW_WIDTH, WINDOW_HEIGHT)
                    self.energizer_pellet_sprite.center_x = x
                    self.energizer_pellet_sprite.center_y = y
                    self.consumable_list.append(self.energizer_pellet_sprite)

                # cherry
                if tile == "c":
                    self.cherry_sprite = Cherry("images/cherry.png", 0.07, WINDOW_WIDTH, WINDOW_HEIGHT)
                    self.cherry_sprite.center_x = x
                    self.cherry_sprite.center_y = y
                    self.consumable_list.append(self.cherry_sprite)

                # strawberry
                if tile == "s":
                    self.strawberry_sprite = Strawberry("images/strawberry.png", 0.09, WINDOW_WIDTH, WINDOW_HEIGHT)
                    self.strawberry_sprite.center_x = x
                    self.strawberry_sprite.center_y = y
                    self.consumable_list.append(self.strawberry_sprite)

                # orange
                if tile == "o":
                    self.orange_sprite = Orange("images/orange.png", 0.07, WINDOW_WIDTH, WINDOW_HEIGHT)
                    self.orange_sprite.center_x = x
                    self.orange_sprite.center_y = y
                    self.consumable_list.append(self.orange_sprite)

                # apple
                if tile == "a":
                    self.apple_sprite = Apple("images/apple.png", 0.1, WINDOW_WIDTH, WINDOW_HEIGHT)
                    self.apple_sprite.center_x = x
                    self.apple_sprite.center_y = y
                    self.consumable_list.append(self.apple_sprite)

                # melon
                if tile == "m":
                    self.melon_sprite = Melon("images/melon.png", 0.1, WINDOW_WIDTH, WINDOW_HEIGHT)
                    self.melon_sprite.center_x = x
                    self.melon_sprite.center_y = y
                    self.consumable_list.append(self.melon_sprite)

                # galaxian
                if tile == "g":
                    self.galaxian_sprite = Galaxian("images/galaxian.png", 0.1, WINDOW_WIDTH, WINDOW_HEIGHT)
                    self.galaxian_sprite.center_x = x
                    self.galaxian_sprite.center_y = y
                    self.consumable_list.append(self.galaxian_sprite)

                # bell
                if tile == "b":
                    self.bell_sprite = Bell("images/bell.png", 0.08, WINDOW_WIDTH, WINDOW_HEIGHT)
                    self.bell_sprite.center_x = x
                    self.bell_sprite.center_y = y
                    self.consumable_list.append(self.bell_sprite)

                # key
                if tile == "k":
                    self.key_sprite = Key("images/key.png", 0.08, WINDOW_WIDTH, WINDOW_HEIGHT)
                    self.key_sprite.center_x = x
                    self.key_sprite.center_y = y
                    self.consumable_list.append(self.key_sprite)


    def on_draw(self):
        self.clear()

        # margin between border = 15
        # margin between path = 50, 45

        # TODO: this could go in its own file eventually (maze class) which would clean up code
        # BORDER GOING AROUND THE GAME
        # Top border (top line)
        arcade.draw_line(100, 600, 797, 600, arcade.color.BLUE, 4)
        # Top border (bottom line, first half)
        arcade.draw_line(115, 585, 455, 585, arcade.color.BLUE, 4)
        # Top border (bottom line, second half)
        arcade.draw_line(470, 585, 782, 585, arcade.color.BLUE, 4)
        # Bottom border (bottom line)
        arcade.draw_line(100, 5, 797, 5, arcade.color.BLUE, 4)
        # Bottom border (top line, first half)
        arcade.draw_line(115, 20, 455, 20, arcade.color.BLUE, 4)
        # Bottom border (top line, second half)
        arcade.draw_line(474, 20, 782, 20, arcade.color.BLUE, 4)

        # Rectangle midway through border (left line)
        arcade.draw_line(457, 487, 457, 587, arcade.color.BLUE, 4)
        # Rectangle midway through border (bottom line)
        arcade.draw_line(455, 485, 474, 485, arcade.color.BLUE, 4)
        # Rectangle midway through border (right line)
        arcade.draw_line(472, 485, 472, 587, arcade.color.BLUE, 4)

        # Rectangle midway through border, mirrored to bottom
        arcade.draw_line(457, 118, 457, 18, arcade.color.BLUE, 4)
        arcade.draw_line(455, 116, 474, 116, arcade.color.BLUE, 4)
        arcade.draw_line(472, 118, 472, 18, arcade.color.BLUE, 4)


        # Left border (left line)
        arcade.draw_line(100, 602, 100, 360, arcade.color.BLUE, 4)
        # Left border (right line)
        arcade.draw_line(115, 587, 115, 375, arcade.color.BLUE, 4)
        # Right border (right line)
        arcade.draw_line(795, 602, 795, 356, arcade.color.BLUE, 4)
        # Right border (left line)
        arcade.draw_line(780, 587, 780, 371, arcade.color.BLUE, 4)

        # Left border - divit halfway through one side, top (top line)
        arcade.draw_line(113, 373, 250, 373, arcade.color.BLUE, 4)
        # Left border - divit halfway through one side, top (bottom line)
        arcade.draw_line(98, 358, 235, 358, arcade.color.BLUE, 4)
        # Left border - divit halfway through one side (vertical line, right)
        arcade.draw_line(250, 326, 250, 375, arcade.color.BLUE, 4)
        # Left border - divit halfway through one side (vertical line, left)
        arcade.draw_line(235, 340, 235, 360, arcade.color.BLUE, 4)
        # Left border - divit halfway through one side, bottom (top line)
        arcade.draw_line(98, 342, 237, 342, arcade.color.BLUE, 4)
        # Left border - divit halfway through one side, bottom (bottom line)
        arcade.draw_line(98, 327, 252, 327, arcade.color.BLUE, 4)

        # Left border, bottom - divit halfway through one side, top (top line)
        arcade.draw_line(98, 277, 250, 277, arcade.color.BLUE, 4)
        # Left border, bottom - divit halfway through one side, top (bottom line)
        arcade.draw_line(98, 262, 235, 262, arcade.color.BLUE, 4)
        # Left border, bottom - divit halfway through one side (vertical line, right)
        arcade.draw_line(250, 230, 250, 279, arcade.color.BLUE, 4)
        # Left border, bottom - divit halfway through one side (vertical line, left)
        arcade.draw_line(235, 244, 235, 264, arcade.color.BLUE, 4)
        # Left border, bottom - divit halfway through one side, bottom (top line)
        arcade.draw_line(98, 244, 237, 244, arcade.color.BLUE, 4)
        # Left border, bottom - divit halfway through one side, bottom (bottom line)
        arcade.draw_line(113, 229, 252, 229, arcade.color.BLUE, 4)

        # Left Border, under the last divit
        # Left border (left line)
        arcade.draw_line(100, 246, 100, 3, arcade.color.BLUE, 4)
        # Left border (right line)
        arcade.draw_line(115, 230, 115, 18, arcade.color.BLUE, 4)


        # RECTANGLES THROUGHOUT THE BOARD
        # Rectangle (top left)
        arcade.draw_lrbt_rectangle_outline(170, 250, 490, 535, arcade.color.BLUE, 4)
        # Rectangle (top left, second over)
        arcade.draw_lrbt_rectangle_outline(295, 410, 490, 535, arcade.color.BLUE, 4)
        # Rectangle (top left, below rectangle to the leftest)
        arcade.draw_lrbt_rectangle_outline(170, 250, 423, 440, arcade.color.BLUE, 4)
        # Rectangle (bottom, leftest most)
        arcade.draw_lrbt_rectangle_outline(170, 250, 70, 184, arcade.color.BLUE, 4)



        # Left divit (top)
        arcade.draw_line(780, 373, 650, 373, arcade.color.BLUE, 4)
        arcade.draw_line(795, 358, 900 - 235, 358, arcade.color.BLUE, 4)
        arcade.draw_line(650, 326, 650, 375, arcade.color.BLUE, 4)
        arcade.draw_line(665, 340, 900 - 235, 360, arcade.color.BLUE, 4)
        arcade.draw_line(797, 342, 663, 342, arcade.color.BLUE, 4)
        arcade.draw_line(797, 327, 648, 327, arcade.color.BLUE, 4)

        # Left divit (bottom)
        arcade.draw_line(797, 277, 650, 277, arcade.color.BLUE, 4)
        arcade.draw_line(797, 262, 665, 262, arcade.color.BLUE, 4)
        arcade.draw_line(650, 230, 650, 279, arcade.color.BLUE, 4)
        arcade.draw_line(665, 244, 665, 264, arcade.color.BLUE, 4)
        arcade.draw_line(795, 244, 663, 244, arcade.color.BLUE, 4)
        arcade.draw_line(780, 229, 648, 229, arcade.color.BLUE, 4)

        # Left border under the last divit
        arcade.draw_line(795, 246, 795, 3, arcade.color.BLUE, 4)
        arcade.draw_line(780, 230, 780, 18, arcade.color.BLUE, 4)

        # Rectangle (top left → top right)
        arcade.draw_lrbt_rectangle_outline(522, 637, 490, 535, arcade.color.BLUE, 4)
        # Rectangle (second over → mirrored to left of right side)
        arcade.draw_lrbt_rectangle_outline(682, 730, 490, 535, arcade.color.BLUE, 4)
        # Rectangle (second over → mirrored to left of right side)
        # Rectangle below first → mirrored
        arcade.draw_lrbt_rectangle_outline(650, 730, 423, 440, arcade.color.BLUE, 4)

        # ghost cage
        # outer rectangle
        arcade.draw_line(360, 240, 550, 240, arcade.color.BLUE, 4)

        # Draw sprites
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
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and setup the GameView
    game = GameView()
    game.setup()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()



if __name__ == "__main__":
    main()
