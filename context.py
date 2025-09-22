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
        self.date_node_size_per = 0.08
        self.date_node_sel_size_per = 0.14
        self.date_node_sel_offsetY_per = 0.045
        self.date_node_smooth_dist = 0.02
        self.date_node_col_low = Color(255, 255, 255, 255)
        self.date_node_col_mid = Color(0, 255, 255, 255)
        self.date_node_col_ser = Color(255, 0, 0, 255)
        self.date_node_sel_color_lerp_white = 0.2
        self.date_node_tc_size_step = {
            "TD": 0.03,
            "TS": 0.06,
            "STS": 0.1,
            "T": 0.13,
            "ST": 0.16,
            "SuperT": 0.2
        }

        self.node_list_view_width_per = 0.58
        self.node_list_view_offsetY = 0.33

        resoH = win.resolution[1]
        self.node_date_font = pygame.font.Font("font/ANTQUABI.TTF", round(resoH*15/540))
        self.node_date_label_font = pygame.font.Font("font/ANTQUABI.TTF", round(resoH*8/540))
        self.info_month_txt_font = pygame.font.Font("font/ANTQUABI.TTF", round(resoH*42/540))
        self.info_month_label_font = pygame.font.Font("font/ANTQUABI.TTF", round(resoH*12/540))
        self.info_tc_name_ch_font = pygame.font.Font("font/NotoSerifCJKsc-Medium.otf", round(resoH*50/540))
        self.info_tc_name_en_font = pygame.font.Font("font/NotoSerifCJKsc-Medium.otf", round(resoH*30/540))
        self.info_tc_type_font = pygame.font.Font("font/BOD_CI.TTF", round(resoH*22/540))

        self.info_pos_left_per = 0.06
        self.info_pos_top_per = 0.05
        self.info_tc_name_offsetX = 0.1
        self.info_tc_name_offset_duration = 1.1

    def close(self):
        self.tkp.quit()
