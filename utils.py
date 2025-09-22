from pygame.color import Color
from pygame.rect import Rect


def color_to_01_tuple3(color: Color) -> tuple:
    norm = color.normalize()
    return norm[:-1]


