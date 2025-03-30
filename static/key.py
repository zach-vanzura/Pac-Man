import arcade

# Set constants for the screen size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Key"

# Open the window. Set the window title and dimensions
arcade.open_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)

# Set the background color
arcade.set_background_color(arcade.color.BLACK)

# Clear screen and start render process
arcade.start_render()

# Draw the center of the blue section
start_x = 300
end_x = 300
start_y = 300
end_y = 350
line_width = 100
BLUE_COLOR = arcade.color.OCEAN_BOAT_BLUE
arcade.draw_line(start_x, start_y, end_x, end_y, BLUE_COLOR, line_width)

# Draw the top of the blue section
start_x = 300
end_x = 300
start_y = 350
end_y = 360
line_width = 40
arcade.draw_line(start_x, start_y, end_x, end_y, BLUE_COLOR, line_width)

# Draw the black cutout of the blue section
start_x = 300
end_x = 300
start_y = 340
end_y = 350
line_width = 40
BLACK_COLOR = arcade.color.BLACK
arcade.draw_line(start_x, start_y, end_x, end_y, BLACK_COLOR, line_width)

# Draw the left part of the silver section
start_x = 290
end_x = 290
start_y = 180
end_y = 300
line_width = 10
SILVER_COLOR = arcade.color.SILVER
arcade.draw_line(start_x, start_y, end_x, end_y, SILVER_COLOR, line_width)

# Draw the top right part of the silver section
x1 = 305
y1 = 300
x2 = 325
y2 = 275
x3 = 305
y3 = 240
arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, SILVER_COLOR)
arcade.draw_triangle_outline(x1, y1, x2, y2, x3, y3, BLACK_COLOR)

# Draw the bottom right part of the silver section
x1 = 305
y1 = 240
x2 = 325
y2 = 210
x3 = 305
y3 = 180
arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, SILVER_COLOR)
arcade.draw_triangle_outline(x1, y1, x2, y2, x3, y3, BLACK_COLOR)

# Draw the bottom of the silver section
x1 = 285
y1 = 180
x2 = 308
y2 = 180
x3 = 297
y3 = 170
arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, SILVER_COLOR)
arcade.draw_triangle_outline(x1, y1, x2, y2, x3, y3, BLACK_COLOR)

# Finish drawing and display the result
arcade.finish_render()

# Keep the window open until the user hits the 'close' button
arcade.run()