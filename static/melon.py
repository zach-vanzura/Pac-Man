import arcade

# Set constants for the screen size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Melon"

# Open the window. Set the window title and dimensions
arcade.open_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)

# Set the background color
arcade.set_background_color(arcade.color.BLACK)

# Clear screen and start render process
arcade.start_render()

# Draw the melon 
x = 300
y = 320
radius = 50
MELON_COLOR = arcade.color.KELLY_GREEN
arcade.draw_circle_filled(x, y, radius, MELON_COLOR)
arcade.draw_circle_outline(x, y, radius, arcade.color.BLACK)

# Draw the vertical melon stem
start_x = 300
end_x = 300
start_y = 362
end_y = 375
STEM_COLOR = arcade.color.DARK_CYAN
line_width = 10
arcade.draw_line(start_x, start_y, end_x, end_y, STEM_COLOR, line_width)

# Draw the horizontal melon stem
start_x = 280
end_x = 320
start_y = 380
end_y = 380
arcade.draw_line(start_x, start_y, end_x, end_y, STEM_COLOR, line_width)

# Draw the little melon stem
start_x = 270
end_x = 280
start_y = 390
end_y = 390
arcade.draw_line(start_x, start_y, end_x, end_y, STEM_COLOR, line_width)

# Draw the blemishes
width = 10
height = 10
LIGHT_COLOR = arcade.color.WHITE

# Left blue curve: T -> B
arcade.draw_ellipse_filled(305, 355, width, height, STEM_COLOR, 90, -1)
arcade.draw_ellipse_outline(305, 355, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(280, 345, width, height, STEM_COLOR, 90, -1)
arcade.draw_ellipse_outline(280, 345, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(265, 325, width, height, STEM_COLOR, 90, -1)
arcade.draw_ellipse_outline(265, 325, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(280, 305, width, height, STEM_COLOR, 90, -1)
arcade.draw_ellipse_outline(280, 305, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(305, 290, width, height, STEM_COLOR, 90, -1)
arcade.draw_ellipse_outline(305, 290, width, height, arcade.color.BLACK, 1, 90)

# Left white curve: T -> B
arcade.draw_ellipse_filled(300, 350, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(300, 350, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(274, 340, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(274, 340, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(260, 320, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(260, 320, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(274, 300, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(274, 300, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(300, 285, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(300, 285, width, height, arcade.color.BLACK, 1, 90)

# Middle blue curve: T -> B
arcade.draw_ellipse_filled(319, 338, width, height, STEM_COLOR, 90, -1)
arcade.draw_ellipse_outline(319, 338, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(295, 325, width, height, STEM_COLOR, 90, -1)
arcade.draw_ellipse_outline(295, 325, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(319, 307, width, height, STEM_COLOR, 90, -1)
arcade.draw_ellipse_outline(319, 307, width, height, arcade.color.BLACK, 1, 90)

# Middle white curve: T -> B
arcade.draw_ellipse_filled(314, 333, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(314, 333, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(290, 320, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(290, 320, width, height, arcade.color.BLACK, 1, 90)

arcade.draw_ellipse_filled(314, 302, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(314, 302, width, height, arcade.color.BLACK, 1, 90)

# Right blue curve: T -> B
arcade.draw_ellipse_filled(335, 325, width, height, STEM_COLOR, 90, -1)
arcade.draw_ellipse_outline(335, 325, width, height, arcade.color.BLACK, 1, 90)

# Right white curve: T -> B
arcade.draw_ellipse_filled(330, 320, width, height, LIGHT_COLOR, 90, -1)
arcade.draw_ellipse_outline(330, 320, width, height, arcade.color.BLACK, 1, 90)


# Finish drawing and display the result
arcade.finish_render()

# Keep the window open until the user hits the 'close' button
arcade.run()