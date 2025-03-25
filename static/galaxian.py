import arcade

# Set constants for the screen size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Galaxian"

# Open the window. Set the window title and dimensions
arcade.open_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)

# Set the background color
arcade.set_background_color(arcade.color.BLACK)

# Clear screen and start render process
arcade.start_render()

# Draw the bottom left half of the blue outter section
x1 = 250
y1 = 290
x2 = 280
y2 = 290
x3 = 280
y3 = 235
OUTTER_SECTION_COLOR = arcade.color.BLUE
arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, OUTTER_SECTION_COLOR)
arcade.draw_triangle_outline(x1, y1, x2, y2, x3, y3, OUTTER_SECTION_COLOR)

# Draw the bottom right half of the blue outter section
x1 = 320
y1 = 290
x2 = 350
y2 = 290
x3 = 320
y3 = 235
arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, OUTTER_SECTION_COLOR)
arcade.draw_triangle_outline(x1, y1, x2, y2, x3, y3, OUTTER_SECTION_COLOR)

# Draw the left half of the yellow midsection
x1 = 255
y1 = 300
x2 = 305
y2 = 300
x3 = 280
y3 = 250
MIDSECTION_COLOR = arcade.color.CYBER_YELLOW
arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, MIDSECTION_COLOR)
arcade.draw_triangle_outline(x1, y1, x2, y2, x3, y3, MIDSECTION_COLOR)

# Draw the right half of the yellow midsection
x1 = 295
y1 = 300
x2 = 345
y2 = 300
x3 = 320
y3 = 250
arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, MIDSECTION_COLOR)
arcade.draw_triangle_outline(x1, y1, x2, y2, x3, y3, MIDSECTION_COLOR)

# Draw the center of the yellow midsection
start_x = 300
end_x = 300
start_y = 265
end_y = 300
line_width = 50
arcade.draw_line(start_x, start_y, end_x, end_y, MIDSECTION_COLOR, line_width)

# Draw the bottom of the yellow midsection
start_x = 300
end_x = 300
start_y = 215
end_y = 280
line_width = 8
arcade.draw_line(start_x, start_y, end_x, end_y, MIDSECTION_COLOR, line_width)

# Draw the main part of the red midsection
x1 = 300
y1 = 325
x2 = 275
y2 = 290
x3 = 325
y3 = 290
RED_COLOR = arcade.color.CORNELL_RED
arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, RED_COLOR)
arcade.draw_triangle_outline(x1, y1, x2, y2, x3, y3, RED_COLOR)

# Draw the center of the red midsection
start_x = 300
end_x = 300
start_y = 280
end_y = 305
line_width = 10
arcade.draw_line(start_x, start_y, end_x, end_y, RED_COLOR, line_width)

# Draw the left cutout of the red midsection in yellow
start_x = 292.5
end_x = 292.5
start_y = 275
end_y = 295
line_width = 7
arcade.draw_line(start_x, start_y, end_x, end_y, MIDSECTION_COLOR, line_width)

# Draw the right cutout of the red midsection in yellow
start_x = 307.5
end_x = 307.5
start_y = 275
end_y = 295
line_width = 7
arcade.draw_line(start_x, start_y, end_x, end_y, MIDSECTION_COLOR, line_width)

# Draw the top left half of the blue outter section
start_x = 254.5
end_x = 254.5
start_y = 290
end_y = 320
line_width = 9
arcade.draw_line(start_x, start_y, end_x, end_y, OUTTER_SECTION_COLOR, line_width)

# Draw the top left half of the blue outter section
start_x = 345.5
end_x = 345.5
start_y = 290
end_y = 320
line_width = 9
arcade.draw_line(start_x, start_y, end_x, end_y, OUTTER_SECTION_COLOR, line_width)


# Finish drawing and display the result
arcade.finish_render()

# Keep the window open until the user hits the 'close' button
arcade.run()