from pico2d import *
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

# 첫 번째 캐릭터 구현
class Al_Run:

    def __init__(self, al):
        self.Al = al

    def enter(self, e):
        # keyup이 아닌 keydown으로 방향을 결정해야 함
        if d_down(e):
            self.Al.dir = self.Al.face_dir = 1
        elif a_down(e):
            self.Al.dir = self.Al.face_dir = -1

    def exit(self, e):
        self.Al.frameX = 0
        pass

    def do(self):
        self.Al.frameX = (self.Al.frameX + 1) % 8
        self.Al.x += self.Al.dir * 10

    def draw(self):
        img = self.Al.images['Al_Run'][int(self.Al.frameX)]
        draw_y = 0 + img.h / 2
        draw_x = self.Al.x
        if self.Al.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

class Al_Idle:

    def __init__(self, al):
        self.Al = al

    def enter(self, e):
        # 멈출 때 이동 방향(dir)만 0으로 하고, face_dir는 현재 바라보는 방향을 유지
        self.Al.dir = 0
    def exit(self, e):
        self.Al.frameX = 0
        pass

    def do(self):
        self.Al.frameX = (self.Al.frameX + 1) % 25
    def draw(self):
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.Al.images['Al_Idle'][int(self.Al.frameX)]
        draw_y = 0 + img.h / 2
        draw_x = self.Al.x
        if self.Al.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)


class Al:
    def __init__(self):
        self.x, self.y = 97, 50
        self.frameX = 0
        self.frameY = 0
        self.face_dir = 1
        self.dir = 1
        self.animation_names = ['Al_Idle', 'Al_Run']
        self.images = {}
        # 각 애니메이션별로 최대 프레임 너비/높이를 저장하면 출력 크기를 통일하여 흔들림을 방지할 수 있음
        self.render_size = {}
        for name in self.animation_names:
            if name == 'Al_Idle':
                frames = [load_image("./AL/" + name + " (%d)" % i + ".png") for i in range(1, 26)]
            elif name == 'Al_Run':
                frames = [load_image("./AL/" + name + " (%d)" % i + ".png") for i in range(1, 9)]
            self.images[name] = frames
            max_w = max(img.w for img in frames)
            max_h = max(img.h for img in frames)
            self.render_size[name] = (max_w, max_h)

        self.IDLE = Al_Idle(self)
        self.RUN = Al_Run(self)
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



# 두 번째 캐릭터 구현
class Jondahl_Run:
    def __init__(self, jondahl):
        self.Jondahl = jondahl

    def enter(self, e):
        # keyup이 아닌 keydown으로 방향을 결정해야 함
        if d_down(e):
            self.Jondahl.dir = self.Jondahl.face_dir = 1
        elif a_down(e):
            self.Jondahl.dir = self.Jondahl.face_dir = -1

    def exit(self, e):
        self.Jondahl.frameX = 0
        pass

    def do(self):
        self.Jondahl.frameX = (self.Jondahl.frameX + 1) % 17
        self.Jondahl.x += self.Jondahl.dir * 10

    def draw(self):
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.Jondahl.images['Jondahl_Run'][int(self.Jondahl.frameX)]
        draw_y = 0 + img.h / 2
        draw_x = self.Jondahl.x
        if self.Jondahl.face_dir < 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

class Jondahl_Idle:
    def __init__(self, jondahl):
        self.Jondahl = jondahl

    def enter(self, e):
        # 멈출 때 이동 방향(dir)만 0으로 하고, face_dir는 현재 바라보는 방향을 유지
        self.Jondahl.dir = 0
    def exit(self, e):
        self.Jondahl.frameX = 0
        pass

    def do(self):
        self.Jondahl.frameX = (self.Jondahl.frameX + 1) % 22
    def draw(self):
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.Jondahl.images['Jondahl_Idle'][int(self.Jondahl.frameX)]
        draw_y = 0 + img.h / 2
        draw_x = self.Jondahl.x
        if self.Jondahl.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

class Jondahl:
    def __init__(self):
        self.x, self.y = 97, 50
        self.frameX = 0
        self.frameY = 0
        self.face_dir = 1
        self.dir = -1
        self.animation_names = ['Jondahl_Idle', 'Jondahl_Run']
        self.images = {}
        self.render_size = {}
        for name in self.animation_names:
            if name == 'Jondahl_Idle':
                frames = [load_image("./Jondahl/" + name + " (%d)" % i + ".png") for i in range(1, 23)]
            elif name == 'Jondahl_Run':
                frames = [load_image("./Jondahl/" + name + " (%d)" % i + ".png") for i in range(1, 18)]
            self.images[name] = frames
            max_w = max(img.w for img in frames)
            max_h = max(img.h for img in frames)
            self.render_size[name] = (max_w, max_h)

        self.IDLE = Jondahl_Idle(self)
        self.RUN = Jondahl_Run(self)
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



# 세 번째 캐릭터 구현
class Zizou_Olympia_Run:

    def __init__(self, zizou_Olympia):
        self.Zizou_Olympia = zizou_Olympia

    def enter(self, e):
        # keyup이 아닌 keydown으로 방향을 결정해야 함
        if d_down(e):
            self.Zizou_Olympia.dir = self.Zizou_Olympia.face_dir = 1
        elif a_down(e):
            self.Zizou_Olympia.dir = self.Zizou_Olympia.face_dir = -1

    def exit(self, e):
        self.Zizou_Olympia.frameX = 0
        pass

    def do(self):
        self.Zizou_Olympia.frameX = (self.Zizou_Olympia.frameX + 1) % 6

        # 이동 처리
        self.Zizou_Olympia.x += self.Zizou_Olympia.dir * 10

    def draw(self):
        # 화면 출력 시 바라보는 방향(face_dir)을 사용해서 멈춰있을 때도 올바른 뒤집기 유지
        img = self.Zizou_Olympia.images['Zizou Olympia_Run'][int(self.Zizou_Olympia.frameX)]
        draw_y = 0 + img.h / 2
        draw_x = self.Zizou_Olympia.x
        if self.Zizou_Olympia.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

class Zizou_Olympia_Idle:

    def __init__(self, zizou_Olympia):
        self.Zizou_Olympia = zizou_Olympia

    def enter(self, e):
        # 멈출 때 이동 방향(dir)만 0으로 하고, face_dir는 현재 바라보는 방향을 유지
        self.Zizou_Olympia.dir = 0
    def exit(self, e):
        self.Zizou_Olympia.frameX = 0
        pass

    def do(self):
        self.Zizou_Olympia.frameX = (self.Zizou_Olympia.frameX + 1) % 15

    def draw(self):
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.Zizou_Olympia.images['Zizou Olympia_Idle'][int(self.Zizou_Olympia.frameX)]
        draw_y = 0 + img.h / 2
        draw_x = self.Zizou_Olympia.x
        if self.Zizou_Olympia.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)



class Zizou_Olympia:
    def __init__(self):
        self.x, self.y = 97, 55
        self.frameX = 0
        self.frameY = 0
        self.face_dir = 1
        self.dir = -1
        self.animation_names = ['Zizou Olympia_Idle', 'Zizou Olympia_Run']
        self.images = {}
        self.render_size = {}
        for name in self.animation_names:
            if name == 'Zizou Olympia_Idle':
                frames = [load_image("./Zizou_Olympia/" + name + " (%d)" % i + ".png") for i in range(1, 16)]
            elif name == 'Zizou Olympia_Run':
                frames = [load_image("./Zizou_Olympia/" + name + " (%d)" % i + ".png") for i in range(1, 7)]
            self.images[name] = frames
            max_w = max(img.w for img in frames)
            max_h = max(img.h for img in frames)
            self.render_size[name] = (max_w, max_h)

        self.IDLE = Zizou_Olympia_Idle(self)
        self.RUN = Zizou_Olympia_Run(self)
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


# 네 번째 캐릭터 구현
class Franzer_Run:

    def __init__(self, franzer):
        self.Franzer = franzer

    def enter(self, e):
        # keyup이 아닌 keydown으로 방향을 결정해야 함
        if d_down(e):
            self.Franzer.dir = self.Franzer.face_dir = 1
        elif a_down(e):
            self.Franzer.dir = self.Franzer.face_dir = -1

    def exit(self, e):
        self.Franzer.frameX = 0
        pass

    def do(self):
        self.Franzer.frameX = (self.Franzer.frameX + 1) % 6
        self.Franzer.x += self.Franzer.dir * 10

    def draw(self):
        img = self.Franzer.images['Franzer_Run'][int(self.Franzer.frameX)]
        draw_y = 0 + img.h / 2
        draw_x = self.Franzer.x
        if self.Franzer.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)


class Franzer_Idle:

    def __init__(self, franzer):
        self.Franzer = franzer

    def enter(self, e):
        # 멈출 때 이동 방향(dir)만 0으로 하고, face_dir는 현재 바라보는 방향을 유지
        self.Franzer.dir = 0
    def exit(self, e):
        # 이미지 리셋
        self.Franzer.frameX = 0
        pass

    def do(self):
        self.Franzer.frameX = (self.Franzer.frameX + 1) % 3
    def draw(self):
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.Franzer.images['Franzer_Idle'][int(self.Franzer.frameX)]
        draw_y = 0 + img.h / 2
        draw_x = self.Franzer.x
        if self.Franzer.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)


class Franzer:
    def __init__(self):
        self.x, self.y = 97, 50
        self.frameX = 0
        self.frameY = 0
        self.face_dir = 1
        self.dir = 1
        self.animation_names = ['Franzer_Idle', 'Franzer_Run']
        self.images = {}
        # 각 애니메이션별로 최대 프레임 너비/높이를 저장하면 출력 크기를 통일하여 흔들림을 방지할 수 있음
        self.render_size = {}
        for name in self.animation_names:
            if name == 'Franzer_Idle':
                frames = [load_image("./Franzer/" + name + " (%d)" % i + ".png") for i in range(1, 4)]
            elif name == 'Franzer_Run':
                frames = [load_image("./Franzer/" + name + " (%d)" % i + ".png") for i in range(1, 7)]
            self.images[name] = frames
            max_w = max(img.w for img in frames)
            max_h = max(img.h for img in frames)
            self.render_size[name] = (max_w, max_h)

        self.IDLE = Franzer_Idle(self)
        self.RUN = Franzer_Run(self)
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

