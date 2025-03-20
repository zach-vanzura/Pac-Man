import arcade

# Set constants for the screen size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Strawberry"

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



# Draw the seeds
width = 15
height = 5
LIGHT_COLOR = arcade.color.WHITE

# Top row: L -> R
arcade.draw_ellipse_filled(260, 410, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(260, 410, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(282, 395, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(282, 395, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(310, 390, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(310, 390, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(338, 395, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(338, 395, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(358, 410, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(358, 410, width, height, arcade.color.BLACK, 1, 90)

# Middle row: L -> R
arcade.draw_ellipse_filled(270, 380, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(270, 380, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(295, 370, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(295, 370, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(325, 370, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(325, 370, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(350, 380, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(350, 380, width, height, arcade.color.BLACK, 1, 90)

# Bottom row: L -> R
arcade.draw_ellipse_filled(282, 355, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(282, 355, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(310, 345, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(310, 345, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(338, 355, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(338, 355, width, height, arcade.color.BLACK, 1, 90)

# Finish drawing and display the result
arcade.finish_render()

# Keep the window open until the user hits the 'close' button
arcade.run()
