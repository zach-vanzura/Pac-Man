import arcade

# Set constants for the screen size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Cherry"

# Open the window. Set the window title and dimensions
arcade.open_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)

# Set the background color
arcade.set_background_color(arcade.color.WHITE)

# Clear screen and start render process
arcade.start_render()

# Draw the left cherry 
x = 300
y = 320
radius = 50
CHERRY_COLOR = arcade.color.CORNELL_RED
arcade.draw_circle_filled(x, y, radius, CHERRY_COLOR)
arcade.draw_circle_outline(x, y, radius, arcade.color.BLACK)

# Draw the right cherry
x = 375
y = 300
radius = 50
arcade.draw_circle_filled(x, y, radius, CHERRY_COLOR)
arcade.draw_circle_outline(x, y, radius, arcade.color.BLACK)


# Draw the left cherry stem
start_x = 312
end_x = 385
start_y = 357
end_y = 455
STEM_COLOR = arcade.color.BROWN_NOSE
line_width = 10
arcade.draw_line(start_x, start_y, end_x, end_y, STEM_COLOR, line_width)

# Draw the right cherry stem
start_x = 375
end_x = 385
start_y = 340
end_y = 455
line_width = 10
arcade.draw_line(start_x, start_y, end_x, end_y, STEM_COLOR, line_width)

# Draw the light on the left cherry
x = 280
y = 350
LIGHT_COLOR = arcade.color.WHITE
arcade.draw_ellipse_filled(x, y, 25, 10, LIGHT_COLOR, 145, -1)

# Draw the light on the right cherry
x = 345
y = 320
arcade.draw_ellipse_filled(x, y, 25, 10, LIGHT_COLOR, 130, -1)

# Finish drawing and display the result
arcade.finish_render()

# Keep the window open until the user hits the 'close' button
arcade.run()
