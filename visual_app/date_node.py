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

from data_fetcher import TCRecord
from tween import Tween, Ease
from utils import *
from visual_app.tc_app_comp import AppButton
import pygame_shaders
from pygame_shaders import Shader


class DateNode(AppButton):
    def __init__(self, ctx:AppContext,
                 rect: Rect, evt_rect: Rect,
                 data: TCRecord, idx: int, color: Color, node_shader_path: str):
        self.date_label: str = "th"
        super().__init__(ctx, rect, self.__get_date_text(data.tc_start_date))
        self.ori_rect = Rect(self.rect)
        self.pointer_evt_rect = Rect(evt_rect)
        self.tc_data: TCRecord = data
        self.idx: int = idx
        self.date_text: Surface = None

        self.img = Surface(self.rect.size, flags=pygame.SRCALPHA)  # create rect using the larger size
        self.img_shader = Shader(pygame_shaders.DEFAULT_VERTEX_SHADER, node_shader_path, self.img)

        self.cur_color: Color = Color(color)  # a copy
        self.ori_color: Color = Color(color)  # a copy
        self.sel_color: Color = self.ori_color.lerp(Color("white"), ctx.date_node_sel_color_lerp_white)
        self.cur_alpha_lerp: float = 1
        self.cur_smooth_dist = ctx.date_node_smooth_dist
        self.ori_smooth_dist = ctx.date_node_smooth_dist

        self.ori_norm_size: float = ctx.date_node_size_per / ctx.date_node_sel_size_per
        self.cur_norm_size: float = self.ori_norm_size  # used for shader

        self.img_sel_color_tween = Tween()
        self.img_scale_tween = Tween()
        self.img_offset_tween = Tween()
        self.alpha_lerp_tween = Tween()
        self.smooth_dist_tween = Tween()

        self.__update_sel_color(self.ori_color)
        self.__update_sel_norm_scale(self.cur_norm_size)
        self.__update_alpha_lerp(self.cur_alpha_lerp)
        self.__update_smooth_dist(self.cur_smooth_dist)
        self.sel_node_duration = 0.3

        # appear animation
        dur = 0.45
        t = Tween()
        t.to_color(self.ctx.clear_white, self.ori_color, dur, self.__update_sel_color, ease=Ease.OutCubic)
        t2 = Tween()
        t2.to_float(0.1, self.cur_norm_size, dur, self.__update_sel_norm_scale, ease=Ease.OutCubic)

    def __get_date_text(self, date: datetime.date) -> str:
        txt: str = date.strftime("%d")
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

    def __update_alpha_lerp(self, v: float):
        self.img_shader.send("alphaLerp", v)
        self.cur_alpha_lerp = v

    def __update_smooth_dist(self, v: float):
        self.img_shader.send("smoothDist", v)
        self.cur_smooth_dist = v

    def update(self):
        ...

    def render(self):
        # render text
        is_mul_of_five = (self.idx+1) % 5 == 0
        is_tc_date = self.tc_data.tc_type_short != "null"
        # if True:
        if is_mul_of_five or is_tc_date:
            color = self.ori_color if is_tc_date else self.ctx.half_clear_white
            self.date_text = self.ctx.node_date_font.render(f"{self.idx + 1}", True, color).convert_alpha()
            self.date_text.set_alpha(color.a)
            txt_rect = self.date_text.get_rect()
            txt_rect.centerx = self.rect.centerx
            txt_rect.top = self.rect.bottom
            txt_rect.y -= self.ctx.win.resolution[1] * self.ctx.date_node_date_text_offsetY
            self.ctx.win.display.blit(self.date_text, txt_rect)

            label = self.ctx.node_date_label_font.render(self.date_label, True, color).convert_alpha()
            label.set_alpha(color.a)
            label_rect = label.get_rect()
            label_rect.midtop = txt_rect.midbottom
            self.ctx.win.display.blit(label, label_rect)

        img = self.img_shader.render(False)  # .convert_alpha()
        self.ctx.win.display.blit(img, self.rect)

    def on_enter(self):
        # print(f"enter {self.text}")
        duration = self.sel_node_duration
        self.img_sel_color_tween.to_color(self.cur_color, self.sel_color, duration, self.__update_sel_color)
        self.img_scale_tween.to_float(self.cur_norm_size, 0.52, duration, self.__update_sel_norm_scale, ease=Ease.OutCubic)
        self.smooth_dist_tween.to_float(self.cur_smooth_dist, self.ctx.date_node_sel_smooth_dist, duration,
                                        self.__update_smooth_dist, ease=Ease.OutCubic)
        offset = self.ctx.win.resolution[1] * self.ctx.date_node_sel_offsetY_per
        self.img_offset_tween.to_float(self.rect.y, self.rect.y - offset, duration, self.__update_sel_offsetY, ease=Ease.OutCubic)
        self.alpha_lerp_tween.to_float(self.cur_alpha_lerp, 0.5, duration*2.2, self.__update_alpha_lerp, ease=Ease.OutCubic)

        # set visual profile
        self.ctx.bg.apply_profile_by_tc_type(self.tc_data.tc_type_short)

        # update info display
        self.ctx.info_display.set_display_data(self.tc_data)

    def on_exit(self):
        # print(f"exit {self.text}")
        duration = self.sel_node_duration
        self.img_sel_color_tween.to_color(self.cur_color, self.ori_color, duration, self.__update_sel_color)
        self.img_scale_tween.to_float(self.cur_norm_size, self.ori_norm_size, duration, self.__update_sel_norm_scale, ease=Ease.OutCubic)
        self.smooth_dist_tween.to_float(self.cur_smooth_dist, self.ori_smooth_dist, duration,
                                        self.__update_smooth_dist, ease=Ease.OutCubic)
        self.img_offset_tween.to_float(self.rect.y, self.ori_rect.y, duration, self.__update_sel_offsetY, ease=Ease.OutCubic)
        self.alpha_lerp_tween.to_float(self.cur_alpha_lerp, 1.0, duration, self.__update_alpha_lerp, ease=Ease.OutCubic)

    def on_click(self):
        # print(f"clicked node {self.idx}")
        pass
