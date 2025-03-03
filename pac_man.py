import arcade

# Set constants for the screen size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Open the window. Set the window title and dimensions
arcade.open_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)

# Set the background color
arcade.set_background_color(arcade.color.WHITE)

# Clear screen and start render process
arcade.start_render()

# Draw the face
x = 300
y = 300
radius = 100
PAC_MAN_COLOR = arcade.color.YELLOW
arcade.draw_arc_filled(300, 300, 200, 200, PAC_MAN_COLOR, 30, 330)

# Draw the right eye
x = 330
y = 355
radius = 14
PAC_MAN_EYE = arcade.color.BLACK
arcade.draw_circle_filled(x, y, radius, PAC_MAN_EYE)

# Finish drawing and display the result
arcade.finish_render()

# Keep the window open until the user hits the 'close' button
arcade.run()