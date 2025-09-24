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
from visual_app.performance import Performance
from visual_app.tc_app_comp import AppComponent
from visual_win import TCVisualWindow
from context import AppContext
from tween import Tween, Ease
from utils import *
from copy import deepcopy


class TCBgProfile:
    """
    Tropical cyclone background profile class, Tropical Storm (TS) pprofile as default
    """

    def __init__(self,
                 col1: Color = Color(49, 75, 85, 255),
                 col2: Color = Color(107, 167, 105, 255),
                 fade_scale: float = 3.0,
                 rot_velocity: float = 0.1,
                 swing_arms: float = 5.4526,
                 density: float = 1.0,
                 move_speed: float = 0.1,
                 noise_detail: float = 2.5):
        self.bg_col1: Color = col1
        self.bg_col2: Color = col2
        self.rot_velocity: float = rot_velocity
        self.swing_arms: float = swing_arms
        self.fade_scale: float = fade_scale
        self.density: float = density
        self.move_speed: float = move_speed
        self.noise_detail = noise_detail


class TCBackground(AppComponent):
    """
    Tropical cyclone background class
    """

    def __init__(self, ctx: AppContext, downscale_rect: Rect, frag_shader_path: str):
        super().__init__(ctx, downscale_rect)
        ctx.bg = self

        p = self.ctx.performance
        if p == Performance.Ultra:
            self.render_target = Surface(ctx.win.resolution)
        else:
            self.render_target = Surface(downscale_rect.size)

        self.efx_shader = Shader(pygame_shaders.DEFAULT_VERTEX_SHADER, frag_shader_path, self.render_target)
        self.efx_shader.send("resolution", self.render_target.get_rect().size)

        self.bg_col1_tween = Tween()
        self.bg_col2_tween = Tween()
        self.tc_fade_tween = Tween()
        self.tc_density_tween = Tween()
        self.tc_swing_tween = Tween()
        self.tc_rot_tween = Tween()
        self.tc_move_tween = Tween()
        self.tc_detail_tween = Tween()

        # profiles defining background effect parameters
        self.tc_type_profile = {
            "null": TCBgProfile(col1=Color(66, 190, 210, 255), col2=Color(39, 80, 164, 255),
                                fade_scale=12, swing_arms=18,
                                density=0.86, move_speed=0.05, noise_detail=0.0),

            "TD": TCBgProfile(col1=Color(45, 171, 185, 255), col2=Color(39, 80, 144, 255),
                              fade_scale=5.2, rot_velocity=0.1, swing_arms=4.6,
                              density=1.57, move_speed=0.05, noise_detail=0.0),

            "TS": TCBgProfile(col1=Color(49, 71, 85, 255), col2=Color(56, 178, 221, 255),
                              fade_scale=3.0, rot_velocity=0.1, swing_arms=4.1,
                              density=1.0, move_speed=0.1, noise_detail=2.5),  # Default

            "STS": TCBgProfile(col1=Color(49, 71, 85, 255), col2=Color(38, 160, 218, 255),
                               fade_scale=4, rot_velocity=2.2, swing_arms=3.55,
                               density=0.5714, move_speed=1.32, noise_detail=2.8336),

            "T": TCBgProfile(col1=Color(49, 71, 85, 255), col2=Color(38, 160, 218, 255),
                             fade_scale=3.3, rot_velocity=5, swing_arms=3.0,
                             density=0.58, move_speed=6.88, noise_detail=4.2),

            "ST": TCBgProfile(col1=Color(16, 40, 56, 255), col2=Color(56, 117, 218, 255),
                              fade_scale=2.07, rot_velocity=10, swing_arms=1.345,
                              density=0.4121, move_speed=12.3,  noise_detail=5),

            "SuperT": TCBgProfile(col1=Color(25, 18, 16, 255), col2=Color(83, 93, 221, 255),
                                  fade_scale=1.2, rot_velocity=16, swing_arms=0.7,
                                  density=0.3, move_speed=18.1, noise_detail=15)
        }

        self.cur_tc_type = ""
        default_tc_type = "TS"
        self.cur_profile: TCBgProfile = deepcopy(self.tc_type_profile[default_tc_type])
        self.apply_profile_by_tc_type(default_tc_type)  # use the default profile

    def __update_col1(self, color: Color):
        self.cur_profile.bg_col1 = color
        self.efx_shader.send("bgColor1", color.normalize())

    def __update_col2(self, color: Color):
        self.cur_profile.bg_col2 = color
        self.efx_shader.send("bgColor2", color.normalize())

    def __update_fade(self, v: float):
        self.cur_profile.fade_scale = v
        self.efx_shader.send("fadeScale", v)

    def __update_density(self, v: float):
        self.cur_profile.density = v
        self.efx_shader.send("density", v)

    def __update_swing(self, v: float):
        self.cur_profile.fade_scale = v
        self.efx_shader.send("swingArms", v)

    def __update_rot(self, v: float):
        self.cur_profile.rot_velocity = v
        self.efx_shader.send("rotVelocity", v)

    def __update_move(self, v: float):
        self.cur_profile.move_speed = v
        self.efx_shader.send("moveSpeed", v)

    def __update_detail(self, v: float):
        self.cur_profile.noise_detail = v
        self.efx_shader.send("noiseDetail", v)

    def apply_profile_by_tc_type(self, tc_type: str):
        if tc_type == self.cur_tc_type:
            return

        self.cur_tc_type = tc_type
        c = self.cur_profile
        d = self.tc_type_profile[tc_type]

        # apply smooth transition
        duration = 3
        self.bg_col1_tween.to_color(c.bg_col1, d.bg_col1, duration, self.__update_col1)
        self.bg_col2_tween.to_color(c.bg_col2, d.bg_col2, duration, self.__update_col2)
        self.tc_fade_tween.to_float(c.fade_scale, d.fade_scale, duration, self.__update_fade)
        self.tc_density_tween.to_float(c.density, d.density, duration, self.__update_density)
        self.tc_swing_tween.to_float(c.swing_arms, d.swing_arms, duration, self.__update_swing)
        self.tc_rot_tween.to_float(c.rot_velocity, d.rot_velocity, 0.7, self.__update_rot)
        self.tc_move_tween.to_float(c.move_speed, d.move_speed, 0.8, self.__update_move)
        self.tc_detail_tween.to_float(c.noise_detail, d.noise_detail, 1.0, self.__update_detail)

    def render(self):
        self.efx_shader.send("time", self.ctx.win.app_time)
        tc_out = self.efx_shader.render(False)

        p = self.ctx.performance
        if p != Performance.Ultra:
            tc_out = pygame.transform.smoothscale(tc_out, self.ctx.win.resolution)
            # pass

        self.ctx.win.display.blit(tc_out, (0, 0))

    def update(self):
        ...
