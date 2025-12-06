import al_profile
import game_framework
import game_world
from pico2d import *

import al_profile
import jondahl_profile
import zizou_olympia_profile
import franzer_profile

import play_mode


def init():
    global running
    global font
    global profiles
    global white_background
    running = True
    font = load_font("./FONT/neodgm.ttf", 50)
    white_background = load_image("./UI/white_background.png")


    profiles = [al_profile.Al_profile(x=560, y=360, w=140, h=200),
        jondahl_profile.Jondahl_profile(x=400, y=360, w=140, h=200),
        zizou_olympia_profile.Zizou_Olympia_profile(x=240, y=360, w=140, h=200),
        franzer_profile.Franzer_profile(x=80, y=360, w=140, h=200),
        al_profile.Al_profile2(x=720, y=360, w=140, h=200),
        jondahl_profile.Jondahl_profile2(x=880, y=360, w=140, h=200),
        zizou_olympia_profile.Zizou_Olympia_profile2(x=1040, y=360, w=140, h=200),
        franzer_profile.Franzer_profile2(x=1200, y=360, w=140, h=200),]

def finish():
    del font, profiles, white_background
    pass
def update():
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mx, my = event.x, 720 - event.y
            left_mouse_areaX, left_mouse_areaY = 700, 500
            right_mouse_areaX, right_mouse_areaY = 1200, 600
            left_mouse_areaX_quit, left_mouse_areaY_quit = 700, 300
            right_mouse_areaX_quit, right_mouse_areaY_quit = 1200, 400
            if left_mouse_areaX <= mx <= right_mouse_areaX and left_mouse_areaY <= my <= right_mouse_areaY:
                game_framework.change_mode(play_mode)
            elif left_mouse_areaX_quit <= mx <= right_mouse_areaX_quit and left_mouse_areaY_quit <= my <= right_mouse_areaY_quit:
                game_framework.quit()


def draw():
    global font, profiles
    clear_canvas()
    white_background.draw(1280 // 2, 720 // 2, 1280, 720)
    draw_rectangle(0, 0, 160, 720, 255,0,128, 100, True)
    draw_rectangle(160, 0, 320, 720, 128,0,128, 100, True)
    draw_rectangle(320, 0, 480, 720, 255,0,128, 100, True)
    draw_rectangle(480, 0, 640, 720, 128,0,128, 100, True)
    draw_rectangle(640, 0, 800, 720, 255,0,128, 100, True)
    draw_rectangle(800, 0, 960, 720, 128,0,128, 100, True)
    draw_rectangle(960, 0, 1120, 720, 255,0,128, 100, True)
    draw_rectangle(1120, 0, 1280, 720, 128,0,128, 100, True)
    for p in profiles:
        p.draw()

    # font.draw(705, 550, 'Start Game', (255, 255, 255))


    update_canvas()

def pause(): pass

def resume(): pass