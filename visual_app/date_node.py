"""
SID: 25098892g
NAME: LUO DONGPU

Node element for date selection.
"""

import math
import datetime
import pygame.mouse
from context import AppContext
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.color import Color

from tween import Tween, Ease
from utils import *
from visual_app.tc_app_comp import AppButton
import pygame_shaders
from pygame_shaders import Shader


class DateNode(AppButton):
    def __init__(self, ctx:AppContext, rect: Rect, date: datetime.datetime, node_shader_path: str):
        super().__init__(ctx, rect, self.__get_date_text(date))
        self.ori_rect = Rect(self.rect)
        self.date_label: str = "th"

        self.img = Surface(self.rect.size, flags=pygame.SRCALPHA)  # create rect using the larger size
        self.img_shader = Shader(pygame_shaders.DEFAULT_VERTEX_SHADER, node_shader_path, self.img)

        self.cur_color: Color = Color(255, 255, 255, 255)
        self.ori_color: Color = Color(255, 255, 255, 255)
        self.sel_color: Color = self.ori_color.lerp(Color("white"), ctx.date_node_sel_color_lerp_white.get())

        self.ori_norm_size: float = ctx.date_node_size_per.get() / ctx.date_node_sel_size_per.get()
        self.cur_norm_size: float = self.ori_norm_size  # used for shader

        self.img_sel_color_tween = Tween()
        self.img_scale_tween = Tween()
        self.img_offset_tween = Tween()

        self.__update_sel_color(self.ori_color)
        self.__update_sel_norm_scale(self.cur_norm_size)
        self.sel_node_duration = 0.3

    def __get_date_text(self, date: datetime.datetime) -> str:
        txt = date.strftime("%d")
        if txt[-1] == "1": self.date_label = "st"
        elif txt[-1] == "2": self.date_label = "nd"
        elif txt[-1] == "3": self.date_label = "rd"
        return txt

    def __update_sel_color(self, col: Color):
        self.img_shader.send("color", col.normalize())
        self.cur_color = col

    def __update_sel_norm_scale(self, v: float):
        self.img_shader.send("scale", v)
        self.cur_norm_size = v

    def __update_sel_offsetY(self, v: float):
        self.rect.y = v

    def update(self):
        self.img_shader.send("smoothDist", self.ctx.date_node_smooth_dist.get())
        pointer_pos: tuple = pygame.mouse.get_pos()
        if self.ori_rect.collidepoint(pointer_pos):
            if not self.is_hover:
                self.is_hover = True
                self.on_enter()
        elif self.is_hover:
            self.is_hover = False
            self.on_exit()

        if self.is_hover:
            if self.ctx.win.is_left_pointer_down:
                self.on_click()

    def render(self):
        img = self.img_shader.render()
        self.ctx.win.display.blit(img, self.rect)
        # TODO: render text

    def on_enter(self):
        # print(f"enter {self.text}")
        duration = self.sel_node_duration
        self.img_sel_color_tween.to_color(self.cur_color, self.sel_color, duration, self.__update_sel_color)
        self.img_scale_tween.to_float(self.cur_norm_size, 1.0, duration, self.__update_sel_norm_scale, ease=Ease.OutCubic)
        offset = self.ctx.win.resolution[1] * self.ctx.date_node_sel_offsetY_per.get()
        self.img_offset_tween.to_float(self.rect.y, self.rect.y - offset, duration, self.__update_sel_offsetY, ease=Ease.OutCubic)
        # TODO: update text

    def on_exit(self):
        # print(f"exit {self.text}")
        duration = self.sel_node_duration
        self.img_sel_color_tween.to_color(self.cur_color, self.ori_color, duration, self.__update_sel_color)
        self.img_scale_tween.to_float(self.cur_norm_size, self.ori_norm_size, duration, self.__update_sel_norm_scale, ease=Ease.OutCubic)
        self.img_offset_tween.to_float(self.rect.y, self.ori_rect.y, duration, self.__update_sel_offsetY, ease=Ease.OutCubic)
        # TODO: update text

    def on_click(self):
        pass
