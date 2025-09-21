import tkparam
from visual_win import TCVisualWindow
from data_fetcher import TCDataFetcher


class AppContext:
    def __init__(self, win: TCVisualWindow, data_fetcher: TCDataFetcher):
        self.win: TCVisualWindow = win
        self.data_fetcher: TCDataFetcher = data_fetcher
        self.tkp = tkparam.TKParamWindow()

        # debugging parameters
        self.fade_scale = self.tkp.get_scalar("fade scale", 2.8856, 3, 80)
        self.rot_speed = self.tkp.get_scalar("rot speed", 0.1, 0, 10)
        self.swing_arms = self.tkp.get_scalar("swing arms", 5.4526, 0.1, 20)

    def close(self):
        self.tkp.quit()
