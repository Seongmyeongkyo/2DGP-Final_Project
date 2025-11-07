from pico2d import *

import game_framework
import game_world

import player1_character
import player2_character


def handle_events():

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
            continue
        # ESC로 종료
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
            continue
        # 키 입력은 키 종류에 따라 각 플레이어로 라우팅
        if event.type in (SDL_KEYDOWN, SDL_KEYUP):
            key = getattr(event, 'key', None)
            # player1: WASD
            if key in (SDLK_w, SDLK_a, SDLK_s, SDLK_d):
                if 'player1' in globals() and hasattr(player1, 'handle_event'):
                    player1.handle_event(event)
                continue
            if key in (SDLK_i, SDLK_k, SDLK_j, SDLK_l):
                if 'player2' in globals() and hasattr(player2, 'handle_event'):
                    player2.handle_event(event)
                continue

        # 그 외 이벤트(마우스 등)는 필요에 따라 모두에게 전달
        if 'player1' in globals() and hasattr(player1, 'handle_event'):
            player1.handle_event(event)
        if 'player2' in globals() and hasattr(player2, 'handle_event'):
            player2.handle_event(event)


def init():
    global player1, player2

    game_world.clear()

    player1 = player1_character.Jondahl()
    game_world.add_object(player1, 1)

    player2 = player2_character.Franzer()
    game_world.add_object(player2, 1)


def update():
    game_world.update()

    game_world.handle_collision()
def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass
