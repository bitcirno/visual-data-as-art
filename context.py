import tkparam
from visual_win import TCVisualWindow
from data_fetcher import TCDataFetcher
from pygame.color import Color


class AppContext:
    def __init__(self, win: TCVisualWindow, data_fetcher: TCDataFetcher):
        self.win: TCVisualWindow = win
        self.data_fetcher: TCDataFetcher = data_fetcher
        self.tkp = tkparam.TKParamWindow()

        # debugging parameters
        self.date_node_size_per = self.tkp.get_scalar("dnode size", 0.078, 0.001, 0.4)
        self.date_node_sel_size_per = self.tkp.get_scalar("dnode sel size", 0.11, 0.001, 0.4)
        self.date_node_sel_offsetY_per = self.tkp.get_scalar("dnode sel offset", 0.03, 0.0001, 0.3)
        self.date_node_col_low = Color(255, 255, 255, 255)
        self.date_node_col_mid = Color(0, 255, 255, 255)
        self.date_node_col_ser = Color(255, 0, 0, 255)
        self.date_node_sel_color_lerp_white = self.tkp.get_scalar("dnode sel color mul", 0.2, 0.0, 1.0)
        self.date_node_smooth_dist = self.tkp.get_scalar("dnode smooth range", 0.01, 0.0, 1.0)

    def close(self):
        self.tkp.quit()
