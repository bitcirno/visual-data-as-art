"""
SID: 25098892g
NAME: LUO DONGPU

Visualizer application component class
"""
from abc import abstractmethod


class TCVisualAppComp:
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
