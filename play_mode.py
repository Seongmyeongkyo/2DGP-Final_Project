from pico2d import *

import game_framework
import game_world

import player1_character
import player2_character
import Play_background
import Hp_Ui
import Mana_Ui


def handle_events():
    global player1, player2

    event_list = get_events()

    # 숫자키로 플레이어 교체 매핑 (없으면 무시)
    player1_key_map = {
        SDLK_1: 'Al',
        SDLK_2: 'Jondahl',
        SDLK_3: 'Zizou_Olympia',
        SDLK_4: 'Franzer',
    }
    player2_key_map = {
        SDLK_6: 'Al',
        SDLK_7: 'Jondahl',
        SDLK_8: 'Zizou_Olympia',
        SDLK_9: 'Franzer',
    }

    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
            continue
        # ESC로 종료
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
            continue

        # 숫자키로 캐릭터 교체 처리 (keydown)
        if event.type == SDL_KEYDOWN:
            key = getattr(event, 'key', None)

            if key in player1_key_map:
                cls_name = player1_key_map[key]
                cls = getattr(player1_character, cls_name, None)
                if cls:
                    # 기존 player1 제거 후 새 객체 추가
                    try:
                        if 'player1' in globals():
                            game_world.remove_object(player1)
                    except Exception:
                        pass
                    player1 = cls()
                    game_world.add_object(player1, 1)
                continue

            if key in player2_key_map:
                cls_name = player2_key_map[key]
                cls = getattr(player2_character, cls_name, None)
                if cls:
                    try:
                        if 'player2' in globals():
                            game_world.remove_object(player2)
                    except Exception:
                        pass
                    player2 = cls()
                    game_world.add_object(player2, 1)
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
    global player1, player2, background, player1_Hp, player2_Hp, player1_Mana, player2_Mana

    game_world.clear()

    background = Play_background.background()
    game_world.add_object(background, 0)

    player1 = player1_character.Al()
    game_world.add_object(player1, 1)

    player2 = player2_character.Al()
    game_world.add_object(player2, 1)

    player1_Hp = Hp_Ui.Player1_Hp_Ui()
    game_world.add_object(player1_Hp, 3)

    player2_Hp = Hp_Ui.Player2_Hp_Ui()
    game_world.add_object(player2_Hp, 3)

    player1_Mana = Mana_Ui.Player1_Mana_Ui()
    game_world.add_object(player1_Mana, 3)

    player2_Mana = Mana_Ui.Player2_Mana_Ui()
    game_world.add_object(player2_Mana, 3)


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
