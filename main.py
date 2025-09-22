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
from visual_app.list_view import HoriNodeListView
from visual_win import TCVisualWindow
from visual_app.tc_background import TCBackground
from visual_app.date_node import DateNode
from context import AppContext
from tween import Tween

pygame.init()
data_fetcher = TCDataFetcher()

reso = (960, 540)
# reso = (960/2*3, 540/2*3)
win = TCVisualWindow(reso)  # Initialize the visual window
ctx = AppContext(win, data_fetcher)  # build application contex

# Initialize the application components
bg = TCBackground(ctx, Rect(0, 0, *reso), "shaders/tropical_cyclone.glsl")
node_list_rect = Rect(0, 0, reso[0]*ctx.node_list_view_width_per, 10)
node_list_rect.center = reso[0]/2, reso[1]/2 + reso[1]*ctx.node_list_view_offsetY
node_list = HoriNodeListView(ctx, node_list_rect)
ctx.bg = bg
ctx.node_list = node_list

# fetch data
data_fetcher.fetch_latest()
data = data_fetcher.tc_records[-31:]
node_list.switch_date_nodes(data)


# img = pygame.image.load("img.png")

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
    bg.update()
    node_list.update()

    # update active tweens
    Tween.update_active_tweens()

    # render app components
    bg.render()
    # win.display.blit(img, (0, 0))
    node_list.render()

    # final blit event by visual window
    win.final_blit_event()


# quit application
win.quit()
pygame.quit()
ctx.close()
