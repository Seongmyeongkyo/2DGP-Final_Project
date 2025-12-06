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
    global choice_player1 # 선택된 캐릭터 저장 변수
    global choice_player2 # 선택된 캐릭터 저장 변수

    running = True
    font = load_font("./FONT/neodgm.ttf", 40)
    white_background = load_image("./UI/white_background.png")

    profiles = [al_profile.Al_profile(x=560, y=360, w=140, h=200),
        jondahl_profile.Jondahl_profile(x=400, y=360, w=140, h=200),
        zizou_olympia_profile.Zizou_Olympia_profile(x=240, y=360, w=140, h=200),
        franzer_profile.Franzer_profile(x=80, y=360, w=140, h=200),
        al_profile.Al_profile2(x=720, y=360, w=140, h=200),
        jondahl_profile.Jondahl_profile2(x=880, y=360, w=140, h=200),
        zizou_olympia_profile.Zizou_Olympia_profile2(x=1040, y=360, w=140, h=200),
        franzer_profile.Franzer_profile2(x=1200, y=360, w=140, h=200),]

    choice_player1 = None
    choice_player2 = None

def finish():
    global font, profiles, white_background, choice_player1, choice_player2
    del font, profiles, white_background, choice_player1, choice_player2
    pass
def update():
    pass

def handle_events():
    global choice_player1
    global choice_player2

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mx, my = event.x, 720 - event.y

            # 마우스 좌표 영역 list 설정
            player1_select_x = [490, 630, 330, 470, 170, 310, 10, 150]
            player1_select_y = [260, 460]
            player2_select_x = [650, 790, 810, 950, 970, 1110, 1130, 1270]
            player2_select_y = [260, 460]

            # player 1 캐릭터 선택 로직
            if player1_select_x[0] <= mx <= player1_select_x[1] and player1_select_y[0] <= my <= player1_select_y[1]:
                print("player 1 selected Al")
                choice_player1 = "Al"
            elif player1_select_x[2] <= mx <= player1_select_x[3] and player1_select_y[0] <= my <= player1_select_y[1]:
                print("player 1 selected Jondahl")
                choice_player1 = "Jondahl"
            elif player1_select_x[4] <= mx <= player1_select_x[5] and player1_select_y[0] <= my <= player1_select_y[1]:
                print("player 1 selected Zizou_Olympia")
                choice_player1 = "Zizou_Olympia"
            elif player1_select_x[6] <= mx <= player1_select_x[7] and player1_select_y[0] <= my <= player1_select_y[1]:
                print("player 1 selected Franzer")
                choice_player1 = "Franzer"

            # player 2 캐릭터 선택 로직
            if player2_select_x[0] <= mx <= player2_select_x[1] and player2_select_y[0] <= my <= player2_select_y[1]:
                print("player 2 selected Al")
                choice_player2 = "Al"
            elif player2_select_x[2] <= mx <= player2_select_x[3] and player2_select_y[0] <= my <= player2_select_y[1]:
                print("player 2 selected Jondahl")
                choice_player2 = "Jondahl"
            elif player2_select_x[4] <= mx <= player2_select_x[5] and player2_select_y[0] <= my <= player2_select_y[1]:
                print("player 2 selected Zizou_Olympia")
                choice_player2 = "Zizou_Olympia"
            elif player2_select_x[6] <= mx <= player2_select_x[7] and player2_select_y[0] <= my <= player2_select_y[1]:
                print("player 2 selected Franzer")
                choice_player2 = "Franzer"



def draw():
    global font, profiles, white_background, choice_player1, choice_player2
    clear_canvas()

    white_background.draw(1280 // 2, 720 // 2, 1280, 720)
    draw_rectangle(0, 0, 1280, 720, 0,0,0, 100, True)
    draw_rectangle(0, 0, 1280, 720, 0,0,0, 100, True)
    draw_rectangle(0, 0, 1280, 720, 0,0,0, 100, True)
    draw_rectangle(640,0, 641, 720, 255,255,255, 100, True)
    font.draw(250, 650, 'Player1', (255, 255, 255))
    font.draw(900, 650, 'Player2', (255, 255, 255))
    if choice_player1 == "Al":
        draw_rectangle(480, 250, 640, 470, 0,255,255, 100, True)
        font.draw(480, 500, 'Selected', (255, 255, 255))
    elif choice_player1 == "Jondahl":
        draw_rectangle(320, 250, 480, 470, 184,248,251, 100, True)
        font.draw(320, 500, 'Selected', (255, 255, 255))
    elif choice_player1 == "Zizou_Olympia":
        draw_rectangle(160, 250, 320, 470, 128,0,128, 100, True)
        font.draw(160, 500, 'Selected', (255, 255, 255))
    elif choice_player1 == "Franzer":
        draw_rectangle(0, 250, 160, 470, 255,0,0, 100, True)
        font.draw(0, 500, 'Selected', (255, 255, 255))

    if choice_player2 == "Al":
        draw_rectangle(640, 250, 800, 470, 0,255,255, 100, True)
        font.draw(640, 500, 'Selected', (255, 255, 255))
    elif choice_player2 == "Jondahl":
        draw_rectangle(800, 250, 960, 470, 184,248,251, 100, True)
        font.draw(800, 500, 'Selected', (255, 255, 255))
    elif choice_player2 == "Zizou_Olympia":
        draw_rectangle(960, 250, 1120, 470, 128,0,128, 100, True)
        font.draw(960, 500, 'Selected', (255, 255, 255))
    elif choice_player2 == "Franzer":
        draw_rectangle(1120, 250, 1280, 470, 255,0,0, 100, True)
        font.draw(1120, 500, 'Selected', (255, 255, 255))

    for p in profiles:
        p.draw()

    # font.draw(705, 550, 'Start Game', (255, 255, 255))

    update_canvas()

def pause(): pass

def resume(): pass