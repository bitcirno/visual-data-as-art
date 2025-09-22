"""
SID: 25098892g
NAME: LUO DONGPU

This script defines commonly used components
"""

from abc import abstractmethod
from pygame.rect import Rect
from context import AppContext


class AppComponent:
    def __init__(self, ctx: AppContext, size: tuple):
        self.ctx: AppContext = ctx
        self.rect: Rect = Rect(0, 0, *size)

    @abstractmethod
    def update(self):
        """
        Update logic
        """
        ...

    @abstractmethod
    def render(self):
        """
        Render graphics
        """
        ...


class AppButton(AppComponent):
    def __init__(self, ctx: AppContext, size: tuple, text: str):
        super().__init__(ctx, size)
        self.text: str = text
        self.is_hover = False  # is the pointer hovering the button?

    @abstractmethod
    def on_enter(self):
        """
        Invoked on pointer entering the rect
        :return:
        """
        ...

    @abstractmethod
    def on_exit(self):
        """
        Invoked on pointer exiting the rect
        """
        ...

    @abstractmethod
    def on_click(self):
        """
        Invoked on clicking in the rect
        """
        ...
