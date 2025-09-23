"""
SID: 25098892g
NAME: LUO DONGPU

A Visualization window which manages main pygame events
"""

import pygame
from pygame.surface import Surface
from pygame.color import Color
import pygame_shaders
import time
import datetime
from dateutil.relativedelta import relativedelta


class TCVisualWindow:
    def __init__(self, resolution: tuple = (960, 540), title: str = "Tropical Cyclone Calendar (TCC)", fps: int = 120):
        self.ctx = None
        self.resolution: tuple = resolution
        self.title: str = title
        self.fps: int = fps

        pygame.display.set_mode(resolution, pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption(f"{title}  FPS: {fps}")

        self.display: Surface = Surface(resolution)
        self.clock = pygame.time.Clock()
        self.__screen_shader = pygame_shaders.DefaultScreenShader(self.display)
        self.__app_start_time: float = time.time()
        self.app_time: float = 0  # accumulated time since app start
        self.delta_time: float = 0  # time since last frame
        self.clear_display_color = Color(0, 0, 0)
        self.display_month: datetime.date = datetime.date.today()

        # events
        self.is_left_pointer_down: bool = False  # is pointer down this frame?

        # real-time fps calculation
        self.fps_accum_target: int = 10
        self.fps_accum_count: int = 0
        self.fps_accum_time: float = 0.0
        self.smoothed_fps: int = fps

    def final_init_app(self):
        # show the CT records of the current month
        data = self.ctx.data_fetcher.get_data_a_month(self.display_month)
        self.ctx.node_list.switch_date_nodes(data)

    def handle_events(self) -> bool:
        self.is_left_pointer_down = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.is_left_pointer_down = True
            if event.type == pygame.MOUSEWHEEL:
                self.switch_month(event.y)
        return False

    def __calculate_smooth_fps(self):
        self.fps_accum_count += 1
        self.fps_accum_time += self.delta_time
        if self.fps_accum_count >= self.fps_accum_target:
            self.smoothed_fps = round(self.fps_accum_count / self.fps_accum_time)
            pygame.display.set_caption(f"{self.title}  FPS: {self.smoothed_fps}")
            self.fps_accum_count = 0
            self.fps_accum_time = 0.0

    def switch_month(self, month_inc: int):
        date_today = datetime.date.today()
        if month_inc > 0:  # to previous month
            if self.display_month.year == 2000 and self.display_month.month == 1:
                return  # cannot before 2000.1
            self.display_month -= relativedelta(months=+1)
        else:  # to next month
            if self.display_month.year == date_today.year and self.display_month.month == date_today.month:
                return  # cannot after the current month
            self.display_month += relativedelta(months=+1)
        data = self.ctx.data_fetcher.get_data_a_month(self.display_month)
        self.ctx.node_list.switch_date_nodes(data)

    def early_update(self):
        """
        Update import data (time etc) at first of a frame
        """
        self.display.fill(self.clear_display_color)
        self.app_time = time.time() - self.__app_start_time
        self.delta_time = self.clock.get_time() / 1000.0
        self.__calculate_smooth_fps()

    def final_blit_event(self):
        self.__screen_shader.render()
        pygame.display.flip()
        self.clock.tick(self.fps)

    def quit(self):
        pass
