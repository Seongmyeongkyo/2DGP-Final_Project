import game_framework
from pico2d import *
from sound_manager import sound_manager
winner = None

def init():
    global image
    global running
    global font
    sound_manager.load_all()
    sound_manager.play_loop('exit', volume=60)
    image = load_image("./UI/" + "white_background" + ".png")
    running = True
    font = load_font("./FONT/neodgm.ttf", 200)

    # play_mode에서 전달받은 승자 정보 사용
    winner = None


def finish():
    global image, font
    del image
    del font
    sound_manager.stop('exit')

def update():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.quit()


def draw():
    global image, font, winner
    clear_canvas()
    image.draw(1280 // 2, 720 // 2, 1280, 720)
    # winner 변수로 승자 결정
    if winner == 'player1':
        font.draw(100, 720 // 2, 'Player1 Win', (255, 255, 0))
    elif winner == 'player2':
        font.draw(100, 720 // 2, 'Player2 Win', (255, 255, 0))

    update_canvas()


def pause():
    pass


def resume():
    pass


def set_winner(winner_name):
    global winner
    winner = winner_name