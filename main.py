"""
SID: 25098892g
NAME: LUO DONGPU

The main loop of the tropical-cyclone-visualizer application
"""

import math
import datetime
import pygame
import pygame_shaders
from pygame.rect import Rect

from data_fetcher import TCDataFetcher
from visual_win import TCVisualWindow
from visual_app.tc_background import TCBackground
from visual_app.date_node import DateNode
from context import AppContext
from tween import Tween

pygame.init()
data_fetcher = TCDataFetcher()

win = TCVisualWindow()  # Initialize the visual window
ctx = AppContext(win, data_fetcher)  # build application contex

# Initialize the application components
# bg = TCBackground(ctx, Rect(0, 0, *win.resolution), "shaders/tropical_cyclone.glsl")
size = math.floor(ctx.win.resolution[1] * ctx.date_node_sel_size_per.get())
node = DateNode(ctx, Rect(win.resolution[0]/2, win.resolution[1]/2, size, size),
                datetime.datetime.now(), "shaders/date_node.glsl")

# Main loop of the application
is_running = True
while is_running:

    # early update of a frame
    win.early_update()

    # handle events
    is_quit = win.handle_events()
    if is_quit:
        break

    # app components update
    # bg.update()
    node.update()

    # update active tweens
    Tween.update_active_tweens()

    # render app components
    # bg.render()
    node.render()

    # final blit event by visual window
    win.final_blit_event()


# quit application
win.quit()
pygame.quit()
ctx.close()
