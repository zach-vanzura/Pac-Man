import arcade

# Set constants for the screen size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Melon"

# Open the window. Set the window title and dimensions
arcade.open_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)

# Set the background color
arcade.set_background_color(arcade.color.WHITE)

# Clear screen and start render process
arcade.start_render()

# Draw the melon 
x = 300
y = 300
width = 150
height = 160
MELON_COLOR = arcade.color.INDIAN_YELLOW # or deep lemon
arcade.draw_ellipse_filled(x, y, width, height, MELON_COLOR, 90, -1)
arcade.draw_ellipse_outline(x, y, width, height, arcade.color.BLACK, 1, 90)

# Draw the bottom half of the leaves
start_x = 300
end_x = 355
start_y = 380
height = 20
LEAF_COLOR = arcade.color.KELLY_GREEN
arcade.draw_parabola_filled(start_x, start_y, end_x, height, LEAF_COLOR, 180)
arcade.draw_parabola_outline(start_x, start_y, end_x, height, arcade.color.BLACK, 1, 180)

# Draw the top half of the leaves
start_x = 300
end_x = 355
start_y = 380
height = 20
arcade.draw_parabola_filled(start_x, start_y, end_x, height, LEAF_COLOR, 0)
arcade.draw_parabola_outline(start_x, start_y, end_x, height, arcade.color.BLACK, 1, 0)

# Draw the stem
start_x = 300
end_x = 300
start_y = 360
end_y = 405
line_width = 10
STEM_COLOR = arcade.color.BROWN_NOSE
arcade.draw_line(start_x, start_y, end_x, end_y, STEM_COLOR, line_width)


# Finish drawing and display the result
arcade.finish_render()

# Keep the window open until the user hits the 'close' button
arcade.run()
