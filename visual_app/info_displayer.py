"""
SID: 25098892g
NAME: LUO DONGPU

This class displays information of tropical cyclones
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
from visual_app.tc_app_comp import AppButton, AppComponent


class InfoDisplayer(AppComponent):
    def __init__(self, ctx: AppContext, rect_topleft: Rect, rect_topright: Rect):
        super().__init__(ctx, rect_topleft)
        ctx.info_display = self
        self.rect_tl = rect_topleft
        self.rect_tr = rect_topright
        self.tc_ch_name: Surface = None
        self.tc_ch_name_rect: Rect = None
        self.tc_en_name: Surface = None
        self.tc_en_name_rect: Rect = None
        self.tc_type: Surface = None
        self.tc_type_rect: Rect = None
        self.tc_signal: Surface = None
        self.tc_signal_rect: Rect = None
        self.tc_time: Surface = None
        self.tc_time_rect: Rect = None

        self.rect_tl_tween = Tween()
        self.rect_tr_tween = Tween()
        self.fade_tween = Tween()

        self.is_tc_node = False

    def __update_text_rect_tl(self, v: float):
        self.tc_ch_name_rect.x = v
        self.__update_relative_rect_tl()

    def __update_text_rect_tr(self, v: float):
        self.tc_signal_rect.right = v
        self.__update_relative_rect_tr()

    def __update_alpha(self, v: float):
        alpha = round(v)
        self.tc_ch_name.set_alpha(alpha)
        self.tc_en_name.set_alpha(alpha)
        self.tc_type.set_alpha(alpha)
        self.tc_signal.set_alpha(alpha)
        self.tc_time.set_alpha(alpha)

    def __update_relative_rect_tl(self):
        self.tc_en_name_rect.topleft = self.tc_ch_name_rect.bottomleft
        self.tc_type_rect.topleft = self.tc_ch_name_rect.topright

    def __update_relative_rect_tr(self):
        self.tc_time_rect.topright = self.tc_signal_rect.bottomright

    def set_display_data(self, data: TCRecord):
        self.is_tc_node = data.tc_type_short != "null"
        self.tc_ch_name = self.ctx.info_tc_name_ch_font.render(data.tc_name_ch, True, self.ctx.white).convert_alpha()
        self.tc_en_name = self.ctx.info_tc_name_en_font.render(data.tc_name_en, True, self.ctx.white).convert_alpha()
        self.tc_type = self.ctx.info_tc_type_font.render(f" {data.tc_type}", True, self.ctx.not_that_white).convert_alpha()
        self.tc_signal = self.ctx.info_tc_type_font.render(
            f"Signal {data.tc_signal} {data.tc_signal_direction}", True, self.ctx.not_that_white).convert_alpha()

        if data.from_last_to == 0: tc_time_text = f"start at {data.tc_start_date.hour}:{data.tc_start_date.minute}"
        elif data.from_last_to == 1: tc_time_text = f"last all day"
        elif data.from_last_to == 2: tc_time_text = f"end at {data.tc_end_date.hour}:{data.tc_end_date.minute}"
        else: tc_time_text = f"from {data.tc_start_date.hour}:{data.tc_start_date.minute} to {data.tc_end_date.hour}:{data.tc_end_date.minute}"
        self.tc_time = self.ctx.info_tc_type_font.render(tc_time_text, True, self.ctx.not_that_white).convert_alpha()

        self.tc_ch_name_rect = self.tc_ch_name.get_rect()
        self.tc_en_name_rect = self.tc_en_name.get_rect()
        self.tc_type_rect = self.tc_type.get_rect()
        self.tc_signal_rect = self.tc_signal.get_rect()
        self.tc_time_rect = self.tc_time.get_rect()

        self.tc_ch_name_rect.topleft = self.rect_tl.topleft
        self.tc_signal_rect.topright = self.rect_tr.topright
        self.__update_relative_rect_tl()
        self.__update_relative_rect_tr()

        duration = self.ctx.info_tc_name_offset_duration
        offset = self.ctx.info_tc_name_offsetX * self.ctx.win.resolution[0]
        self.fade_tween.to_float(0.0, 255.0, duration, self.__update_alpha, ease=Ease.OutQuad)
        self.rect_tl_tween.to_float(self.rect_tl.x - offset, self.rect_tl.x,
                                    duration * 0.3, self.__update_text_rect_tl, ease=Ease.OutCubic)
        if self.is_tc_node:  # Draw if there is TC
            self.rect_tr_tween.to_float(self.rect_tr.right + offset, self.rect_tr.right,
                                        duration * 0.3, self.__update_text_rect_tr, ease=Ease.OutCubic)

    def update(self):
        pass

    def render(self):
        if not self.tc_ch_name:
            return

        self.ctx.win.display.blit(self.tc_ch_name, self.tc_ch_name_rect)
        self.ctx.win.display.blit(self.tc_en_name, self.tc_en_name_rect)
        self.ctx.win.display.blit(self.tc_type, self.tc_type_rect)
        if self.is_tc_node:
            self.ctx.win.display.blit(self.tc_signal, self.tc_signal_rect)
            self.ctx.win.display.blit(self.tc_time, self.tc_time_rect)
