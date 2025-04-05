import arcade

# Set constants for the screen size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Pac-Man Logo"

# Open the window. Set the window title and dimensions
arcade.open_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)

# Set the background color
arcade.set_background_color(arcade.color.ORANGE)

# Clear screen and start render process
arcade.start_render()




# Finish drawing and display the result
arcade.finish_render()

# Keep the window open until the user hits the 'close' button
arcade.run()