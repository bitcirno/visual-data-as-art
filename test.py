"""
SID: 25098892g
NAME: LUO DONGPU
"""

import pygame
import pygame_shaders
from pygame_shaders import Shader
import time
import tkparam
from pyglm import glm

pygame.init()

param_win = tkparam.TKParamWindow()
fade_scale = param_win.get_scalar("fade scale", 3.0, 0, 80)
rot_speed = param_win.get_scalar("rot speed", 0.1, 0, 100)
swing_arms = param_win.get_scalar("swing arms", 5.4526, 0.1, 20)
density = param_win.get_scalar("density", 1, 0.1, 5)
move_speed = param_win.get_scalar("move speed", 0.1, 0, 20)
noise_scale = param_win.get_scalar("noise detail", 2.6, 0, 20)
bg_color1 = pygame.Color(49, 71, 85, 255)
bg_color2 = pygame.Color(38, 160, 218, 255)

resolution = (960, 540)
fps = 60
pygame.display.set_mode(resolution, pygame.DOUBLEBUF | pygame.OPENGL)
display = pygame.surface.Surface(resolution)

clock = pygame.time.Clock()

hurricane_shader = Shader(pygame_shaders.DEFAULT_VERTEX_SHADER, "shaders/tropical_cyclone.glsl", display)
hurricane_shader.send("resolution", resolution)
hurricane_shader.send("bgColor1", bg_color1.normalize())
hurricane_shader.send("bgColor2", bg_color2.normalize())

screen_shader = pygame_shaders.DefaultScreenShader(display)

start_time = time.time()

is_running = True

def recompile_shader(mod_shader, vertex_path, fragment_path):
    mod_shader.shader = Shader.create_vertfrag_shader(mod_shader.ctx, vertex_path, fragment_path)


while is_running:
    shader_time = time.time() - start_time
    display.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    if not is_running:
        break

    hurricane_shader.send("time", shader_time)
    hurricane_shader.send("fadeScale", fade_scale.get())
    hurricane_shader.send("rotVelocity", rot_speed.get())
    hurricane_shader.send("swingArms", swing_arms.get())
    hurricane_shader.send("density", density.get())
    hurricane_shader.send("moveSpeed", move_speed.get())
    hurricane_shader.send("noiseDetail", noise_scale.get())
    hurricane = hurricane_shader.render(False)
    display.blit(hurricane, (0, 0))

    screen_shader.render()  # finally blit display surface to OpenGL screen
    pygame.display.flip()
    clock.tick(fps)


pygame.quit()
param_win.quit()
