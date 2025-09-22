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
        self.date_node_size_per = self.tkp.get_scalar("dnode size", 0.23, 0.001, 0.4)
        self.date_node_sel_size_per = self.tkp.get_scalar("dnode sel size", 0.3, 0.001, 0.4)
        self.date_node_sel_offsetX_per = self.tkp.get_scalar("dnode sel offset", 0.003, 0.0001, 0.3)
        self.date_node_col_low = Color(255, 255, 255, 255)
        self.date_node_col_mid = Color(0, 255, 255, 255)
        self.date_node_col_ser = Color(255, 0, 0, 255)
        self.date_node_sel_color_mul = self.tkp.get_scalar("dnode sel color mul", 1.1, 0.01, 2)

    def close(self):
        self.tkp.quit()
