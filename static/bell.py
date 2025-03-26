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

# Draw the body of the bell 
start_x = 240
end_x = 370
start_y = 0
height = 270
BELL_COLOR = arcade.color.BANANA_YELLOW
arcade.draw_parabola_filled(start_x, start_y, end_x, height, BELL_COLOR, 0)
arcade.draw_parabola_outline(start_x, start_y, end_x, height, arcade.color.BLACK, 2, 0)

# Draw the top of the bell
x = 305
y = 405
radius = 10
arcade.draw_circle_filled(x, y, radius, BELL_COLOR, 180)
arcade.draw_circle_outline(x, y, radius, arcade.color.BLACK, 3, 180)

# Draw the bottom of the bell 
start_x = 240
end_x = 370
start_y = 230
height = 40
BOTTOM_COLOR = arcade.color.LIGHT_BLUE
arcade.draw_parabola_filled(start_x, start_y, end_x, height, BOTTOM_COLOR, 0)
arcade.draw_parabola_outline(start_x, start_y, end_x, height, arcade.color.BLACK, 3, 0)

# Draw the bottom line for the bell 
start_x = 240
end_x = 370
start_y = 270
end_y = 270
line_width = 2
LINE_COLOR = arcade.color.BLACK
arcade.draw_line(start_x, start_y, end_x, end_y, LINE_COLOR, line_width)

# Draw the chime for the bell 
start_x = 325
end_x = 325
start_y = 270
end_y = 290
line_width = 10
CHIME_COLOR = arcade.color.LIGHT_GRAY
arcade.draw_line(start_x, start_y, end_x, end_y, CHIME_COLOR, line_width)

# Draw the top shadow 
x = 275
y = 360
width = 50
height = 4
SHADOW_COLOR = arcade.color.BLACK
arcade.draw_ellipse_filled(x, y, width, height, SHADOW_COLOR, 115, -1)
arcade.draw_ellipse_outline(x, y, width, height, arcade.color.BLACK, 1, 115)

# Draw the bottom shadow 
x = 260
y = 315
width = 30
height = 3
arcade.draw_ellipse_filled(x, y, width, height, SHADOW_COLOR, 103, -1)
arcade.draw_ellipse_outline(x, y, width, height, arcade.color.BLACK, 1, 103)

# Finish drawing and display the result
arcade.finish_render()

# Keep the window open until the user hits the 'close' button
arcade.run()
