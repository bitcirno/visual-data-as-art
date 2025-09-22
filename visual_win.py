"""
SID: 25098892g
NAME: LUO DONGPU

A Visualization window which manages main pygame events
"""

import pygame
from pygame.surface import Surface
from pygame.color import Color
import pygame_shaders
from pygame_shaders import Shader
import time
from pyglm import glm


class TCVisualWindow:
    def __init__(self, resolution: tuple = (960, 540), title: str = "Tropical cyclone visualizer", fps: int = 120):
        self.resolution: tuple = resolution
        self.title: str = title
        self.fps: int = fps

        pygame.display.set_mode(resolution, pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption(title)

        self.display: Surface = Surface(resolution)
        self.clock = pygame.time.Clock()
        self.__screen_shader = pygame_shaders.DefaultScreenShader(self.display)
        self.__app_start_time: float = time.time()
        self.app_time: float = 0  # accumulated time since app start
        self.delta_time: float = 0  # time since last frame
        self.clear_display_color = Color(0, 0, 0)

        # events
        self.is_left_pointer_down: bool = False  # is pointer down this frame?

    def handle_events(self) -> bool:
        self.is_left_pointer_down = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.is_left_pointer_down = True
        return False

    def early_update(self):
        """
        Update import data (time etc) at first of a frame
        """
        self.display.fill(self.clear_display_color)
        self.app_time = time.time() - self.__app_start_time
        self.delta_time = self.clock.get_time() / 1000.0

    def final_blit_event(self):
        self.__screen_shader.render()
        pygame.display.flip()
        self.clock.tick(self.fps)

    def quit(self):
        pass
