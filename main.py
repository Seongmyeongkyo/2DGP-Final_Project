from pico2d import *

import player1_character
import player2_character

WIDTH, HEIGHT = 1280, 720

# Game object class here


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
            continue
        # ESC로 종료
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
            continue
        # 키 입력은 키 종류에 따라 각 플레이어로 라우팅
        if event.type in (SDL_KEYDOWN, SDL_KEYUP):
            key = getattr(event, 'key', None)
            # player1: WASD
            if key in (SDLK_w, SDLK_a, SDLK_s, SDLK_d):
                if 'player1' in globals() and hasattr(player1, 'handle_event'):
                    player1.handle_event(event)
                continue
            # player2: 화살표
            if key in (SDLK_UP, SDLK_DOWN, SDLK_LEFT, SDLK_RIGHT):
                if 'player2' in globals() and hasattr(player2, 'handle_event'):
                    player2.handle_event(event)
                continue

        # 그 외 이벤트(마우스 등)는 필요에 따라 모두에게 전달
        if 'player1' in globals() and hasattr(player1, 'handle_event'):
            player1.handle_event(event)
        if 'player2' in globals() and hasattr(player2, 'handle_event'):
            player2.handle_event(event)



def reset_world():
    global world
    global player1
    global player2

    world = []

    player1 = player1_character.Jondahl()
    world.append(player1)

    player2 = player2_character.Al()
    world.append(player2)


def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


running = True



open_canvas(WIDTH, HEIGHT)
reset_world()


# game loop
while running:

    handle_events()
    update_world()
    render_world()
    delay(0.03)
# finalization code
close_canvas()
