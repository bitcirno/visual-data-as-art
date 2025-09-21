"""
SID: 25098892g
NAME: LUO DONGPU
"""

import pygame
import pygame_shaders
from pygame_shaders import Shader
import time
import tkparam
from pyglm import glm

pygame.init()
param_win = tkparam.TKParamWindow()
entity_scale = param_win.get_scalar("entity scale", 2.8856, 3, 80)
rot_speed = param_win.get_scalar("rot speed", 0.1, 0, 10)
swing_arms = param_win.get_scalar("swing arms", 5.4526, 0.1, 20)
bg_color1 = (49.0/255, 71.0/255, 85.0/255)
bg_color2 = (38.0/255, 160.0/255, 218.0/255)


class TCVisualWindow:
    def __init__(self):
        ...
