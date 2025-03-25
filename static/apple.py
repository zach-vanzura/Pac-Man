import arcade

# Set constants for the screen size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Apple"

# Open the window. Set the window title and dimensions
arcade.open_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)

# Set the background color
arcade.set_background_color(arcade.color.BLACK)

# Clear screen and start render process
arcade.start_render()

# Draw the apple 
x = 300
y = 320
radius = 50
APPLE_COLOR = arcade.color.CORNELL_RED
arcade.draw_circle_filled(x, y, radius, APPLE_COLOR)
arcade.draw_circle_outline(x, y, radius, arcade.color.BLACK)

# Draw the apple stem
start_x = 302
end_x = 307
start_y = 362
end_y = 395
STEM_COLOR = arcade.color.BROWN_NOSE
line_width = 10
arcade.draw_line(start_x, start_y, end_x, end_y, STEM_COLOR, line_width)

# Draw the light on the apple
x = 325
y = 305
width = 30
height = 10
LIGHT_COLOR = arcade.color.WHITE
arcade.draw_ellipse_filled(x, y, width, height, LIGHT_COLOR, 120, -1)
arcade.draw_ellipse_outline(x, y, width, height, arcade.color.BLACK, 1, 120)


# Finish drawing and display the result
arcade.finish_render()

# Keep the window open until the user hits the 'close' button
arcade.run()