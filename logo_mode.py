import game_framework
from pico2d import *

import play_mode


def init():
    global image
    global running
    global font

    image = load_image("./UI/" + "game_start" + ".png")
    running = True
    font = load_font("./FONT/neodgm.ttf", 100)

def finish():
    global image
    del image

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
    global image
    global font
    clear_canvas()
    image.draw(1280 // 2, 720 // 2, 1280, 720)

    draw_rectangle(700, 500, 1200, 600, 128,0,128, 100, True)
    font.draw(705, 550, 'Game Start', (255, 255, 255))

    draw_rectangle(700, 300, 1200, 400, 128,0,128, 100, True)
    font.draw(730, 345, 'Exit Game', (255, 255, 255))


    update_canvas()

def pause(): pass

def resume(): pass

