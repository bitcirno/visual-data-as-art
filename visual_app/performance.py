"""
SID: 25098892g
NAME: LUO DONGPU

The tropical cyclones utilized ray marching drawing which is GPU-costing!
This class provides performance setting to run this app on devices with less computational power
"""

from enum import Enum


class Performance(Enum):
    Low = 0
    High = 1
    Ultra = 2
