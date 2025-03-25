import arcade

# Set constants for the screen size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Bell"

# Open the window. Set the window title and dimensions
arcade.open_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)

# Set the background color
arcade.set_background_color(arcade.color.WHITE)

# Clear screen and start render process
arcade.start_render()

# Draw the bottom of the strawberry 
start_x = 250
end_x = 370
start_y = 250
height = 160
STRAWBERRY_COLOR = arcade.color.CORNELL_RED
arcade.draw_parabola_filled(start_x, start_y, end_x, height, STRAWBERRY_COLOR, 180)
arcade.draw_parabola_outline(start_x, start_y, end_x, height, arcade.color.BLACK, 1, 180)

# Draw the top of the strawberry
start_x = 250
end_x = 370
start_y = 330
height = 80
arcade.draw_parabola_filled(start_x, start_y, end_x, height, STRAWBERRY_COLOR, 0)
arcade.draw_parabola_outline(start_x, start_y, end_x, height, arcade.color.BLACK, 1, 0)

# Draw the bottom half of the leaves
start_x = 265
end_x = 355
start_y = 375
height = 60
LEAF_COLOR = arcade.color.KELLY_GREEN
arcade.draw_parabola_filled(start_x, start_y, end_x, height, LEAF_COLOR, 180)
arcade.draw_parabola_outline(start_x, start_y, end_x, height, arcade.color.BLACK, 1, 180)

# Draw the top half of the leaves
start_x = 265
end_x = 355
start_y = 405
height = 30
arcade.draw_parabola_filled(start_x, start_y, end_x, height, LEAF_COLOR, 0)
arcade.draw_parabola_outline(start_x, start_y, end_x, height, arcade.color.BLACK, 1, 0)

# Draw the stem
start_x = 310
end_x = 310
start_y = 440
end_y = 465
line_width = 10
STEM_COLOR = arcade.color.BROWN_NOSE
arcade.draw_line(start_x, start_y, end_x, end_y, STEM_COLOR, line_width)

# Finish drawing and display the result
arcade.finish_render()

# Keep the window open until the user hits the 'close' button
arcade.run()