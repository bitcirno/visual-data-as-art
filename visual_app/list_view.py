"""
SID: 25098892g
NAME: LUO DONGPU

This class groups and manages all AppComponent is a list view
"""

import math
import pygame
from pygame import Surface
from pygame.rect import Rect
from data_fetcher import TCData
from visual_app.tc_app_comp import AppContext, AppComponent
from visual_app.date_node import DateNode


class HoriNodeListView(AppComponent):

    months_str = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
        5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
        9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }

    def __init__(self, ctx: AppContext, rect: Rect):
        super().__init__(ctx, rect.size)
        self.rect = rect
        self.count: int = 0
        self.nodes = []
        self.cur_sel_node: DateNode = None

        self.node_size = math.floor(ctx.win.resolution[1] * ctx.date_node_sel_size_per)
        self.node_shader_path = "shaders/date_node.glsl"

        self.month_text: Surface = None
        self.month_text_rect: Rect = None
        self.month_label: Surface = None
        self.month_label_rect: Rect = None

    def clear_date_nodes(self):
        for i in range(self.count-1, -1, -1):
            del self.nodes[i]
        self.nodes.clear()

    def switch_date_nodes(self, data: list[TCData]):
        if len(data) == 0:
            return

        if len(self.nodes) > 0:
            self.clear_date_nodes()  # clear previous nodes

        size_offset = self.__get_node_size_offset(data)  # get size weights, sever types will affect neighbor nodes

        posY = self.rect.centery
        self.count = len(data)
        if self.count == 1:
            size = self.node_size + size_offset[0]
            rect = Rect(0, 0, size, size)
            rect.center = self.rect.centerx, posY
            node = DateNode(self.ctx, rect, data[0], 0, self.node_shader_path)
            self.nodes.append(node)
            return

        posX = self.rect.left
        step = self.rect.width / (self.count - 1)
        for i in range(self.count):
            x = posX + i*step
            size = self.node_size + size_offset[i]
            rect = Rect(0, 0, size, size)
            rect.center = x, posY
            node = DateNode(self.ctx, rect, data[i], i, self.node_shader_path)
            self.nodes.append(node)

        first_node = self.nodes[0]
        month = first_node.tc_data.tc_start_date.month
        self.month_text = self.ctx.info_month_txt_font.render(HoriNodeListView.months_str[month], True, "white")
        self.month_text_rect = self.month_text.get_rect()
        self.month_text_rect.midright = first_node.rect.midleft
        self.month_label = self.ctx.info_month_label_font.render(str(first_node.tc_data.tc_start_date.year), True, "white")
        self.month_label_rect = self.month_label.get_rect()
        self.month_label_rect.midtop = self.month_text_rect.midbottom

    def __get_node_size_offset(self, data: list[TCData]) -> list[float]:
        length = len(data)
        if length == 0:
            return [None]
        if length == 1:
            return [self.ctx.dnode_type_size_impact[data[0].tc_type]]

        ret = [0.0] * length
        swin = self.ctx.dnode_impact_half_win_length
        dwt = self.ctx.dnode_size_weights_dist
        imp = self.ctx.dnode_type_size_impact
        for i in range(length):
            offset = 0
            for c in range(max(i-swin,0), min(i+swin,length)):
                dist_w = dwt[abs(i-c)]
                impact = imp[data[c].tc_type_short]
                offset += dist_w * impact
                ret[i] = offset
        # print(ret)
        return ret

    def update(self):
        pointer_pos: tuple = pygame.mouse.get_pos()
        found_first_hover = False
        for node in self.nodes:
            if node.pointer_evt_rect.collidepoint(pointer_pos) and not found_first_hover:
                found_first_hover = True

                if node.is_hover:
                    continue
                node.is_hover = True
                node.on_enter()
                self.cur_sel_node = node
            else:
                if not node.is_hover:
                    continue
                node.is_hover = False
                node.on_exit()

        if self.cur_sel_node and self.cur_sel_node.is_hover:
            if self.ctx.win.is_left_pointer_down:
                self.cur_sel_node.on_click()

    def render(self):
        if len(self.nodes) == 0:
            return

        # render nodes
        for node in self.nodes:
            node.render()

        # render month text
        self.ctx.win.display.blit(self.month_text, self.month_text_rect)
        self.ctx.win.display.blit(self.month_label, self.month_label_rect)

