from pico2d import *

import game_framework
import game_world

import Character_Select_Screen
import player1_character
import player2_character
import Play_background
import Hp_Ui
import Mana_Ui
import Exit_mode
from sound_manager import sound_manager


def handle_events():
    global player1, player2

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
                if 'player2' in globals() and hasattr(player2, 'handle_event'):
                    player2.handle_event(event)
                    continue

        # 그 외 이벤트(마우스 등)는 필요에 따라 모두에게 전달
        if 'player1' in globals() and hasattr(player1, 'handle_event'):
            player1.handle_event(event)
        if 'player2' in globals() and hasattr(player2, 'handle_event'):
            player2.handle_event(event)


def init():
    global player1, player2, background, player1_Hp, player2_Hp, player1_Mana, player2_Mana

    game_world.clear()
    sound_manager.load_all()
    sound_manager.play_loop('background', volume=32)

    background = Play_background.background()
    game_world.add_object(background, 0)

    p1_choice, p2_choice = Character_Select_Screen.get_choices()

    # 기본 캐릭터 설정
    if p1_choice is None:
        p1_choice = 'Al'
    if p2_choice is None:
        p2_choice = 'Al'

    # 실제 캐릭터 클래스 생성
    player1 = getattr(player1_character, p1_choice)()
    game_world.add_object(player1, 1)
    game_world.add_collision_pair('player1:player2', player1, None)

    player2 = getattr(player2_character, p2_choice)()
    game_world.add_object(player2, 1)
    game_world.add_collision_pair('player1:player2', None, player2)

    game_world.add_collision_pair('player2_skill:player1', None, player1)
    game_world.add_collision_pair('player1_skill:player2', None, player2)

    player1_Hp = Hp_Ui.Player1_Hp_Ui()
    game_world.add_object(player1_Hp, 2)

    player2_Hp = Hp_Ui.Player2_Hp_Ui()
    game_world.add_object(player2_Hp, 2)

    player1_Mana = Mana_Ui.Player1_Mana_Ui()
    game_world.add_object(player1_Mana, 2)

    player2_Mana = Mana_Ui.Player2_Mana_Ui()
    game_world.add_object(player2_Mana, 2)


def update():
    game_world.update()

    game_world.handle_collision()

    if player1_Hp.width <= 0:
        # Player1의 체력이 0 이하 -> Player2 승리
        Exit_mode.set_winner('player2')
        game_framework.change_mode(Exit_mode)

    elif player2_Hp.width <= 0:
        # Player2의 체력이 0 이하 -> Player1 승리
        Exit_mode.set_winner('player1')
        game_framework.change_mode(Exit_mode)
def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    sound_manager.stop('background')
    game_world.clear()
def pause(): pass
def resume(): pass
