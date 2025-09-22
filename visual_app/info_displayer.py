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

from data_fetcher import TCData
from tween import Tween, Ease
from utils import *
from visual_app.tc_app_comp import AppButton, AppComponent


class InfoDisplayer(AppComponent):
    def __init__(self, ctx: AppContext, rect: Rect):
        super().__init__(ctx, rect)
        self.tc_ch_name: Surface = None
        self.tc_ch_name_rect: Rect = None
        self.tc_en_name: Surface = None
        self.tc_en_name_rect: Rect = None
        self.tc_type: Surface = None
        self.tc_type_rect: Rect = None

        self.rect_tween = Tween()
        self.fade_tween = Tween()

    def __update_text_rect(self, v: float):
        self.tc_ch_name_rect.x = v
        self.__update_relative_rect()

    def __update_alpha(self, v: float):
        alpha = round(v)
        self.tc_ch_name.set_alpha(alpha)
        self.tc_en_name.set_alpha(alpha)
        self.tc_type.set_alpha(alpha)

    def set_display_data(self, data: TCData):
        self.tc_ch_name = self.ctx.info_tc_name_ch_font.render(data.tc_name_ch, True, "white").convert_alpha()
        self.tc_en_name = self.ctx.info_tc_name_en_font.render(data.tc_name_en, True, "white").convert_alpha()
        self.tc_type = self.ctx.info_tc_type_font.render(f" {data.tc_type}", True, "white").convert_alpha()
        self.tc_ch_name_rect = self.tc_ch_name.get_rect()
        self.tc_en_name_rect = self.tc_en_name.get_rect()
        self.tc_type_rect = self.tc_type.get_rect()
        self.tc_ch_name_rect.topleft = self.rect.topleft
        self.__update_relative_rect()

        duration = self.ctx.info_tc_name_offset_duration
        offset = self.ctx.info_tc_name_offsetX * self.ctx.win.resolution[0]
        self.rect_tween.to_float(self.rect.x-offset, self.rect.x,
                                 duration*0.3, self.__update_text_rect, ease=Ease.OutCubic)
        self.fade_tween.to_float(0.0, 255.0, duration, self.__update_alpha, ease=Ease.OutQuad)

    def __update_relative_rect(self):
        self.tc_en_name_rect.topleft = self.tc_ch_name_rect.bottomleft
        self.tc_type_rect.topleft = self.tc_ch_name_rect.topright

    def update(self):
        pass

    def render(self):
        if not self.tc_ch_name:
            return

        self.ctx.win.display.blit(self.tc_ch_name, self.tc_ch_name_rect)
        self.ctx.win.display.blit(self.tc_en_name, self.tc_en_name_rect)
        self.ctx.win.display.blit(self.tc_type, self.tc_type_rect)

