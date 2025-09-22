"""
SID: 25098892g
NAME: LUO DONGPU

The main loop of the tropical-cyclone-visualizer application
"""
import datetime

import pygame
import pygame_shaders

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
# bg = TCBackground(ctx, "shaders/tropical_cyclone.glsl")
node = DateNode(ctx, datetime.datetime.now(), "shaders/date_node.glsl")

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
