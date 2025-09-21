"""
SID: 25098892g
NAME: LUO DONGPU

Hurricane background, using TCBgProfile to switch effects (rotation speed, color, etc)
"""

import pygame
import pygame_shaders
from pygame.color import Color
from pygame.surface import Surface
from pygame_shaders import Shader
from visual_app.tc_app_comp import TCVisualAppComp
from visual_win import TCVisualWindow
from context import AppContext
from tween import Tween, Ease
from utils import *


class TCBgProfile:
    """
    Tropical cyclone background profile class
    """
    def __init__(self,
                 col1: Color = Color(49, 71, 85, 255),
                 col2: Color = Color(38, 160, 218, 255),
                 rot_velocity: float = 0.1,
                 swing_arms: float = 8.0,
                 fade_scale: float = 2.8856,
                 density: float = 1.0,
                 move_speed: float = 0.1):
        self.bg_col1: Color = col1
        self.bg_col2: Color = col2
        self.rot_velocity: float = rot_velocity
        self.swing_arms: float = swing_arms
        self.fade_scale: float = fade_scale
        self.density: float = density
        self.move_speed: float = move_speed


class TCBackground(TCVisualAppComp):
    """
    Tropical cyclone background class
    """

    def __init__(self, ctx: AppContext, frag_shader_path: str):
        self.ctx: AppContext = ctx
        self.efx_shader = Shader(pygame_shaders.DEFAULT_VERTEX_SHADER, frag_shader_path, ctx.win.display)
        self.efx_shader.send("resolution", ctx.win.resolution)

        self.bg_col1_tween = Tween()
        self.bg_col2_tween = Tween()
        self.tc_fade_tween = Tween()
        self.tc_density_tween = Tween()
        self.tc_swing_tween = Tween()
        self.tc_rot_tween = Tween()
        self.tc_move_tween = Tween()

        # profiles defining background effect parameters
        self.tc_type_profile = {
            "TD": TCBgProfile(col1=Color(255, 255, 255, 255),
                              fade_scale=19.663, rot_velocity=0.0, swing_arms=18.408),
            "TS": TCBgProfile(),
            "STS": TCBgProfile(),
            "T": TCBgProfile(),
            "ST": TCBgProfile(fade_scale=3.0, rot_velocity=7.51, swing_arms=5.2,
                              density=0.2298, move_speed=5.5949),
            "SuperT": TCBgProfile()
        }
        self.cur_profile: TCBgProfile = TCBgProfile()
        self.apply_profile(self.cur_profile)  # use the default profile

        self.trigger = False

    def update_col1(self, color: Color):
        self.cur_profile.bg_col1 = color
        self.efx_shader.send("bgColor1", color_to_01_tuple3(color))

    def update_col2(self, color: Color):
        self.cur_profile.bg_col2 = color
        self.efx_shader.send("bgColor2", color_to_01_tuple3(color))

    def update_fade(self, v: float):
        self.cur_profile.fade_scale = v
        self.efx_shader.send("fadeScale", v)

    def update_density(self, v: float):
        self.cur_profile.density = v
        self.efx_shader.send("density", v)

    def update_swing(self, v: float):
        self.cur_profile.fade_scale = v
        self.efx_shader.send("swingArms", v)

    def update_rot(self, v: float):
        self.cur_profile.rot_velocity = v
        self.efx_shader.send("rotVelocity", v)

    def update_move(self, v: float):
        self.cur_profile.move_speed = v
        self.efx_shader.send("moveSpeed", v)

    def apply_profile(self, profile: TCBgProfile):
        c = self.cur_profile
        d = profile

        # apply smooth transition
        duration = 3
        self.bg_col1_tween.to_color(c.bg_col1, d.bg_col1, duration, self.update_col1)
        self.bg_col2_tween.to_color(c.bg_col2, d.bg_col2, duration, self.update_col2)
        self.tc_fade_tween.to_float(c.fade_scale, d.fade_scale, duration, self.update_fade)
        self.tc_density_tween.to_float(c.density, d.density, duration, self.update_density)
        self.tc_swing_tween.to_float(c.swing_arms, d.swing_arms, duration, self.update_swing)
        self.tc_rot_tween.to_float(c.rot_velocity, d.rot_velocity, 0.7, self.update_rot)
        self.tc_move_tween.to_float(c.move_speed, d.move_speed, 0.8, self.update_move)

    def render(self):
        self.efx_shader.send("time", self.ctx.win.app_time)
        hurricane = self.efx_shader.render()
        self.ctx.win.display.blit(hurricane, (0, 0))

    def update(self):
        pointer_pos = pygame.mouse.get_pos()
        if pointer_pos[0] < 30:
            if not self.trigger:
                self.trigger = True
                self.apply_profile(self.tc_type_profile["TS"])
                print("-> TS")
        elif pointer_pos[0] > 200:
            if self.trigger:
                self.trigger = False
                self.apply_profile(self.tc_type_profile["ST"])
                print("-> ST")
        pass




