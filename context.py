import pygame.font

from visual_app.performance import Performance
# import tkparam

from visual_win import TCVisualWindow
from data_fetcher import TCDataFetcher
from pygame.color import Color


class AppContext:
    def __init__(self, win: TCVisualWindow, performance: Performance, data_fetcher: TCDataFetcher):
        self.win: TCVisualWindow = win
        self.win.ctx = self
        self.data_fetcher: TCDataFetcher = data_fetcher
        self.performance: Performance = performance
        # self.tkp = tkparam.TKParamWindow()

        self.bg = None
        self.node_list = None
        self.info_display = None

        # parameters
        # date node
        self.date_node_size_per = 0.06
        self.date_node_sel_size_per = 0.14
        self.date_node_sel_offsetY_per = 0.045
        self.date_node_smooth_dist = 0.02
        self.date_node_sel_smooth_dist = 0.21
        self.date_node_col_low = Color(255, 255, 255, 255)
        self.date_node_col_mid = Color(0, 255, 255, 255)
        self.date_node_col_ser = Color(255, 0, 0, 255)
        self.date_node_sel_color_lerp_white = 0.2
        self.date_node_date_text_offsetY = 0.02

        self.dnode_impact_half_win_length = 5
        self.dnode_size_weights_dist = [0.0, 0.6, 0.35, 0.15, 0.05, 0.01]
        self.dnode_type_size_impact = {
            "null": 0.0,
            "TD": 11,
            "TS": 13,
            "STS": 15,
            "T": 18,
            "ST": 24,
            "SuperT": 30
        }

        # color definition
        self.white = Color(250, 250, 250, 255)
        self.not_that_white = Color(230, 230, 230, 235)
        self.half_clear_white = Color(200, 200, 200, 128)
        self.clear_white = Color(250, 250, 250, 0)

        self.node_size_offset_max = 42
        self.nodes_gradient_col1 = Color(230, 230, 230, 120)
        self.nodes_gradient_col2 = Color(230, 250, 250, 230)
        self.nodes_gradient_thresh = 0.23

        # node list view
        self.node_list_view_width_per = 0.53
        self.node_list_view_offsetY = 0.3

        # TC information display
        resoH = win.resolution[1]
        self.node_date_font = pygame.font.Font("font/ANTQUABI.TTF", round(resoH*15/540))
        self.node_date_label_font = pygame.font.Font("font/ANTQUABI.TTF", round(resoH*8/540))
        self.info_month_txt_font = pygame.font.Font("font/ANTQUABI.TTF", round(resoH*28/540))
        self.info_month_label_font = pygame.font.Font("font/ANTQUABI.TTF", round(resoH*13/540))
        self.info_tc_name_ch_font = pygame.font.Font("font/NotoSerifCJKsc-Medium.otf", round(resoH*45/540))
        self.info_tc_name_en_font = pygame.font.Font("font/NotoSerifCJKsc-Medium.otf", round(resoH*25/540))
        self.info_tc_type_font = pygame.font.Font("font/BOD_CI.TTF", round(resoH*22/540))

        self.info_pos_left_per = 0.056
        self.info_pos_top_per = 0.09
        self.info_tc_name_offsetX = 0.1
        self.info_tc_name_offset_duration = 1.1

    def close(self):
        # self.tkp.quit()
        pass
