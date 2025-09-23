import pygame.font
import tkparam

from visual_win import TCVisualWindow
from data_fetcher import TCDataFetcher
from pygame.color import Color


class AppContext:
    def __init__(self, win: TCVisualWindow, data_fetcher: TCDataFetcher):
        self.win: TCVisualWindow = win
        self.data_fetcher: TCDataFetcher = data_fetcher
        self.tkp = tkparam.TKParamWindow()

        self.bg = None
        self.node_list = None
        self.info_display = None

        # debugging parameters
        self.date_node_size_per = 0.06
        self.date_node_sel_size_per = 0.14
        self.date_node_sel_offsetY_per = 0.045
        self.date_node_smooth_dist = 0.02
        self.date_node_col_low = Color(255, 255, 255, 255)
        self.date_node_col_mid = Color(0, 255, 255, 255)
        self.date_node_col_ser = Color(255, 0, 0, 255)
        self.date_node_sel_color_lerp_white = 0.2
        self.date_node_date_text_offsetY = 0.01

        self.dnode_impact_half_win_length = 6
        self.dnode_size_weights_dist = [0.0, 0.8, 0.56, 0.35, 0.15, 0.05, 0.01]
        self.dnode_type_size_impact = {
            "": 0.0,
            "TD": 12,
            "TS": 15,
            "STS": 17,
            "T": 20,
            "ST": 23,
            "SuperT": 26
        }

        self.node_list_view_width_per = 0.5
        self.node_list_view_offsetY = 0.33

        resoH = win.resolution[1]
        self.node_date_font = pygame.font.Font("font/ANTQUABI.TTF", round(resoH*15/540))
        self.node_date_label_font = pygame.font.Font("font/ANTQUABI.TTF", round(resoH*8/540))
        self.info_month_txt_font = pygame.font.Font("font/ANTQUABI.TTF", round(resoH*28/540))
        self.info_month_label_font = pygame.font.Font("font/ANTQUABI.TTF", round(resoH*13/540))
        self.info_tc_name_ch_font = pygame.font.Font("font/NotoSerifCJKsc-Medium.otf", round(resoH*50/540))
        self.info_tc_name_en_font = pygame.font.Font("font/NotoSerifCJKsc-Medium.otf", round(resoH*30/540))
        self.info_tc_type_font = pygame.font.Font("font/BOD_CI.TTF", round(resoH*22/540))

        self.info_pos_left_per = 0.06
        self.info_pos_top_per = 0.05
        self.info_tc_name_offsetX = 0.1
        self.info_tc_name_offset_duration = 1.1

    def close(self):
        self.tkp.quit()
