import arcade

# Set constants for the screen size
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
WINDOW_TITLE = "Single_Wall"

# Open the window. Set the window title and dimensions
arcade.open_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)

# Set the background color
arcade.set_background_color(arcade.color.GRAY)

# Clear screen and start render process
arcade.start_render()

# Draw the center blue section
start_x = 0
end_x = 400
start_y = 200
end_y = 200
line_width = 50
BLUE_COLOR = arcade.color.BLUE
arcade.draw_line(start_x, start_y, end_x, end_y, BLUE_COLOR, line_width)

# Finish drawing and display the result
arcade.finish_render()

# Keep the window open until the user hits the 'close' button
arcade.run()