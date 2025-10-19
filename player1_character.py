from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_w, SDLK_s, SDLK_a, SDLK_d

from state_machine import StateMachine

# 이벤트를 체크하는 함수들을 구현
# e = state_event

def time_out(e):
    return e[0] == 'TIMEOUT'

def w_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w
def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def a_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a
def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d
def d_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d


class Run:

    def __init__(self, al):
        self.Al = al

    def enter(self, e):
        # keyup이 아닌 keydown으로 방향을 결정해야 함
        if d_down(e):
            self.Al.dir = self.Al.face_dir = 1
        elif a_down(e):
            self.Al.dir = self.Al.face_dir = -1

    def exit(self, e):
        pass

    def do(self):
        self.Al.frameX = (self.Al.frameX + 1) % 8
        self.Al.frameY = 2
        self.Al.x += self.Al.dir * 5

    def draw(self):
        # 화면 출력 시 바라보는 방향(face_dir)을 사용해서 멈춰있을 때도 올바른 뒤집기 유지
        flip = 'none' if self.Al.face_dir == -1 else 'h'
        self.Al.image.clip_composite_draw(self.Al.frameX * 194, self.Al.frameY * 194, 194, 194, 0, flip, self.Al.x, 90, 194, 194)

class Idle:

    def __init__(self, al):
        self.Al = al

    def enter(self, e):
        # 멈출 때 이동 방향(dir)만 0으로 하고, face_dir는 현재 바라보는 방향을 유지
        self.Al.dir = 0
    def exit(self, e):
        pass

    def do(self):
        self.Al.frameX = (self.Al.frameX + 1) % 8
        self.Al.frameY = 10
    def draw(self):
        flip = 'none' if self.Al.face_dir == -1 else 'h'
        self.Al.image.clip_composite_draw(self.Al.frameX * 194, self.Al.frameY * 194, 194, 194, 0, flip, self.Al.x, 90, 194, 194)



class Al:
    def __init__(self):
        self.x, self.y = 97, 90
        self.frameX = 0
        self.frameY = 0
        self.face_dir = 1
        self.dir = 1
        self.image = load_image('character_Al.png')

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {w_down: self.IDLE, s_down: self.IDLE, a_down : self.RUN, d_down :self.RUN},
                self.RUN : {d_up : self.IDLE, a_up : self.IDLE, a_down : self.RUN, d_down : self.RUN},
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 들어온 외부 키입력 등을 상태 머신에 전달하기 위해서
        # 튜플화 시킨 후, 전달
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
