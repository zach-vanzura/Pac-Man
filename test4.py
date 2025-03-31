import arcade
import random
import math

# Constants
SPRITE_SCALING = 0.025
GHOST_SCALING = 0.075
SPRITE_SIZE = 32
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 720
PACMAN_SPEED = 2
GHOST_SPEED = 1
TILE_SIZE = 36
WINDOW_TITLE = "PAC-MAN"
WALL_SCALING = TILE_SIZE / 128


class Controllable(arcade.Sprite):
    def __init__(self, path_to_sprite, scale, window_width, window_height):
        super().__init__(path_to_sprite, scale=scale)
        self.center_x = window_width / 2
        self.center_y = window_height / 2
        self.window_width = window_width
        self.window_height = window_height
        self.is_edible = False

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.right = self.window_width
        elif self.right > self.window_width:
            self.left = 0

        if self.bottom < 0:
            self.top = self.window_height
        elif self.top > self.window_height:
            self.bottom = 0


class Ghost(Controllable):
    def __init__(self, path_to_sprite, scale, ghost_type, player, window_width, window_height, blinky=None):
        super().__init__(path_to_sprite, scale, window_width, window_height)
        self.ghost_type = ghost_type
        self.player = player
        self.blinky = blinky
        self.point_value = 200

    def get_target_tile(self):
        pacman_tile = (self.player.center_x // TILE_SIZE, self.player.center_y // TILE_SIZE)
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
        target_x, target_y = [t * TILE_SIZE for t in self.get_target_tile()]
        self.change_x = GHOST_SPEED if self.center_x < target_x else -GHOST_SPEED if self.center_x > target_x else 0
        self.change_y = GHOST_SPEED if self.center_y < target_y else -GHOST_SPEED if self.center_y > target_y else 0
        super().update(delta_time)


class Player(Controllable):
    def __init__(self, path_to_sprite, scale, window_width, window_height):
        super().__init__(path_to_sprite, scale, window_width, window_height)
        self.is_dead = False

    def update(self, delta_time: float = 1 / 60):
        super().update(delta_time)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.player_list = None
        self.ghost_list = None
        self.wall_list = None
        self.player_sprite = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.physics_engine = None
        self.ghost_physics_engines = []  # Physics engines for ghosts
        self.background_color = arcade.color.BLACK

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=128)

        self.player_sprite = Player("images/pacman.png", SPRITE_SCALING, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.player_sprite.center_x = WINDOW_WIDTH / 2
        self.player_sprite.center_y = (WINDOW_HEIGHT / 2) - 200
        self.player_list.append(self.player_sprite)

        ghost_types = ["Blinky", "Inky", "Pinky", "Clyde"]
        ghost_images = [f"images/{name.lower()}.png" for name in ghost_types]
        ghosts = []
        for i, (img, g_type) in enumerate(zip(ghost_images, ghost_types)):
            ghost = Ghost(img, GHOST_SCALING, g_type, self.player_sprite, WINDOW_WIDTH, WINDOW_HEIGHT)
            ghost.center_x += (i * 50) - 75
            ghost.center_y += 200
            self.ghost_list.append(ghost)
            ghosts.append(ghost)
        for g in ghosts:
            if g.ghost_type == "Inky":
                g.blinky = ghosts[0]

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        self.ghost_physics_engines = [arcade.PhysicsEngineSimple(g, self.wall_list) for g in self.ghost_list]

        self.setup_maze_walls()
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        self.ghost_physics_engines = []
        for ghost in self.ghost_list:
            engine = arcade.PhysicsEngineSimple(ghost, self.wall_list)
            self.ghost_physics_engines.append(engine)

    def setup_maze_walls(self):
        """
        Set up the maze walls based on a grid layout.
        'X' represents a wall and ' ' represents an open space.
        The maze is centered in the window.
        """
        # 20 lines of 24 characters
        maze = [
            "XXXXXXXXXXXXXXXXXXXXXXXX",
            "X                      X",
            "X                      X",
            "X  XX              XX  X",
            "X  XX              XX  X",
            "X                      X",
            "X                      X",
            "X                      X",
            "XXXX                XXXX",
            "                        ",
            "                        ",
            "                        ",
            "XXXX                XXXX",
            "X                      X",
            "X                      X",
            "X  XX              XX  X",
            "X  XX              XX  X",
            "X                      X",
            "X                      X",
            "XXXXXXXXXXXXXXXXXXXXXXXX"
        ]
        rows = len(maze)
        cols = len(maze[0])
        offset_x = (WINDOW_WIDTH - (cols * TILE_SIZE)) / 2
        offset_y = (WINDOW_HEIGHT - (rows * TILE_SIZE)) / 2

        for row_index, row in enumerate(maze):
            for col_index, char in enumerate(row):
                if char == "X":
                    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", scale=WALL_SCALING)
                    wall.center_x = col_index * TILE_SIZE + TILE_SIZE / 2 + offset_x
                    wall.center_y = (rows - row_index - 1) * TILE_SIZE + TILE_SIZE / 2 + offset_y
                    self.wall_list.append(wall)

    def on_draw(self):
        self.clear()
        self.player_list.draw()
        self.ghost_list.draw()
        self.wall_list.draw()
        arcade.draw_text(f"Score: {self.score}", 10, 10, arcade.color.WHITE, 18)

    def update_player_speed(self):
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed:
            self.player_sprite.change_y = PACMAN_SPEED
        elif self.down_pressed:
            self.player_sprite.change_y = -PACMAN_SPEED
        if self.left_pressed:
            self.player_sprite.change_x = -PACMAN_SPEED
        elif self.right_pressed:
            self.player_sprite.change_x = PACMAN_SPEED

    def on_update(self, delta_time):
        self.update_player_speed()
        self.physics_engine.update()
        self.player_list.update()

        for ghost in self.ghost_list:
            ghost.update(delta_time)
        for engine in self.ghost_physics_engines:
            engine.update()

        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.ghost_list)
        for ghost in hit_list:
            if ghost.is_edible:
                ghost.remove_from_sprite_lists()
                self.score += ghost.point_value

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        self.update_player_speed()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        self.update_player_speed()

    def on_show_view(self):
        self.up_pressed = self.down_pressed = self.left_pressed = self.right_pressed = False


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    game.setup()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
