"""
SID: 25098892g
NAME: LUO DONGPU

This class groups and manages all AppComponent is a list view
"""

import math
from visual_app.tc_app_comp import AppContext, AppComponent
from pygame.rect import Rect


class ListView(AppComponent):
    def __init__(self, ctx: AppContext, rect: Rect):
        super().__init__(ctx, rect.size)
        self.rect = rect