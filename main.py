from pico2d import *
import game_framework

import logo_mode as start_mode

open_canvas(1280, 720)
SDL_SetRenderDrawBlendMode(pico2d.renderer, SDL_BLENDMODE_BLEND)
game_framework.run(start_mode)
close_canvas()