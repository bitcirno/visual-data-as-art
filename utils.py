from pygame.color import Color


def color_to_01_tuple3(color: Color) -> tuple:
    return color.r / 255.0, color.g / 255.0, color.b / 255.0

