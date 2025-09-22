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

    def update(self):
        pass

    def render(self):
        ...

