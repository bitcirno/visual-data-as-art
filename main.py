"""
SID: 25098892g
NAME: LUO DONGPU

Find some challenge!
The main loop of the tropical-cyclone-visualizer application
"""

import pygame
from pygame.rect import Rect

from data_fetcher import TCDataFetcher
from visual_app.info_displayer import InfoDisplayer
from visual_app.list_view import HoriNodeListView
from visual_app.performance import Performance
from visual_win import TCVisualWindow
from visual_app.tc_background import TCBackground
from context import AppContext
from tween import Tween

"""
Recommended to only modify the parameters below!
"""
performance = Performance.Low  # one of Low, High, Ultra, as detailed below

p = min(max(performance.value, 0), 2)
resolution: tuple[int, int] = [(960, 540), (1440, 810), (1440, 810)][p]
downscale_per: float = [4, 2, 1][p]
downscale_reso: tuple[int, int] = round(resolution[0]/downscale_per), round(resolution[1]/downscale_per)
fps: int = [60, 60, 120][p]
print(f"{'[App]': <8} Launched with resolution: {resolution}, FPS: {fps}")

"""
End of parameter modification region.
"""

pygame.init()
data_fetcher = TCDataFetcher()
data_fetcher.fetch_latest()

# initialize the visual window and create app contex
win = TCVisualWindow(resolution, fps=fps)
ctx = AppContext(win, performance, data_fetcher)

# create app components
bg = TCBackground(ctx, Rect(0, 0, *downscale_reso), "shaders/tropical_cyclone.glsl")

node_list_rect = Rect(0, 0, resolution[0] * ctx.node_list_view_width_per, 10)
node_list_rect.center = resolution[0] / 2, resolution[1] / 2 + resolution[1] * ctx.node_list_view_offsetY
node_list = HoriNodeListView(ctx, node_list_rect)

info_display_rect_tl = Rect(resolution[0] * ctx.info_pos_left_per, resolution[1] * ctx.info_pos_top_per, 1, 1)
info_display_rect_tr = Rect(info_display_rect_tl)
info_display_rect_tr.right = resolution[0] * (1 - ctx.info_pos_left_per)
info_display = InfoDisplayer(ctx, info_display_rect_tl, info_display_rect_tr)

# initiate app states
win.final_init_app()

# app main loop
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
    info_display.update()

    # update active tweens
    Tween.update_active_tweens()

    # render app components
    bg.render()
    node_list.render()
    info_display.render()

    # final blit event by visual window
    win.final_blit_event()


# quit application
win.quit()
pygame.quit()
ctx.close()
print(f"{'[App]': <8} Quit")
