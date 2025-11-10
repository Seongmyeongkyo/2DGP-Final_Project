from pico2d import *
from state_machine import StateMachine
import game_world
import game_framework

from olympia_attack import Olympia_attack

# 이벤트를 체크하는 함수들을 구현
# e = state_event

def time_out(e):
    return e[0] == 'TIMEOUT'

def i_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_i
def k_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_k

def j_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_j
def j_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_j
def l_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_l
def l_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_l
def u_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_u

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# 첫 번째 캐릭터 구현
class Al_Attack:

    def __init__(self, al):
        self.Al = al

    def enter(self, e):
        if l_down(e):
            self.Al.dir = self.Al.face_dir = 1
        elif j_down(e):
            self.Al.dir = self.Al.face_dir = -1

    def exit(self, e):
        self.Al.frameX = 0
        pass

    def do(self):

        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.Al.frames_per_animation.get('Al_Attack', 1)

        self.Al.TIME_PER_ACTION = 0.3
        self.Al.ACTION_PER_TIME = 1.0 / self.Al.TIME_PER_ACTION

        increment = length * self.Al.ACTION_PER_TIME * game_framework.frame_time
        self.Al.frameX = (self.Al.frameX + increment) % length

        if self.Al.frameX >= length - 1:
            self.Al.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.Al.images['Al_Attack'][int(self.Al.frameX)]
        draw_y = 0 + img.h / 2
        draw_x = self.Al.x
        if self.Al.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

class Al_Run:

    def __init__(self, al):
        self.Al = al

    def enter(self, e):
        # keyup이 아닌 keydown으로 방향을 결정해야 함
        if l_down(e):
            self.Al.dir = self.Al.face_dir = 1
        elif j_down(e):
            self.Al.dir = self.Al.face_dir = -1

    def exit(self, e):
        self.Al.frameX = 0
        pass

    def do(self):
        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.Al.frames_per_animation.get('Al_Run', 1)

        self.Al.TIME_PER_ACTION = 1.0
        self.Al.ACTION_PER_TIME = 1.0 / self.Al.TIME_PER_ACTION

        increment = length * self.Al.ACTION_PER_TIME * game_framework.frame_time
        self.Al.frameX = (self.Al.frameX + increment) % length

        # 이동 처리
        self.Al.x += self.Al.dir * RUN_SPEED_PPS * game_framework.frame_time

        # 화면과 충돌시 캐릭터가 화면 밖으로 벗어나지 않도록 처리
        img = self.Al.images['Al_Run'][int(self.Al.frameX)]
        if self.Al.x < img.w / 2:
            self.Al.x = img.w / 2
        elif self.Al.x > 1280 - img.w / 2:
            self.Al.x = 1280 - img.w / 2

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

        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.Al.frames_per_animation.get('Al_Idle', 1)

        self.Al.TIME_PER_ACTION = 2.0
        self.Al.ACTION_PER_TIME = 1.0 / self.Al.TIME_PER_ACTION

        increment = length * self.Al.ACTION_PER_TIME * game_framework.frame_time
        self.Al.frameX = (self.Al.frameX + increment) % length

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
        self.x, self.y = 1280-97, 50
        self.frameX = 0
        self.frameY = 0
        self.face_dir = -1
        self.dir = 1
        self.animation_names = ['Al_Idle', 'Al_Run', 'Al_Attack']
        self.images = {}
        # 각 애니메이션별로 최대 프레임 너비/높이를 저장하면 출력 크기를 통일하여 흔들림을 방지할 수 있음
        self.render_size = {}

        self.TIME_PER_ACTION = 2.0
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        # per-animation frame count 저장
        self.frames_per_animation = {}

        for name in self.animation_names:
            if name == 'Al_Idle':
                frames = [load_image("./AL/" + name + " (%d)" % i + ".png") for i in range(1, 24)]
            elif name == 'Al_Run':
                frames = [load_image("./AL/" + name + " (%d)" % i + ".png") for i in range(1, 9)]
            elif name == 'Al_Attack':
                frames = [load_image("./AL/" + name + " (%d)" % i + ".png") for i in range(1, 6)]
            self.images[name] = frames
            max_w = max(img.w for img in frames)
            max_h = max(img.h for img in frames)
            self.render_size[name] = (max_w, max_h)
            self.frames_per_animation[name] = len(frames)

        self.IDLE = Al_Idle(self)
        self.RUN = Al_Run(self)
        self.ATTACK = Al_Attack(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {i_down: self.IDLE, k_down: self.IDLE, j_down : self.RUN, l_down :self.RUN, u_down : self.ATTACK},
                self.RUN : {l_up : self.IDLE, j_up : self.IDLE, j_down : self.RUN, l_down : self.RUN, u_down : self.ATTACK},
                self.ATTACK : {time_out : self.IDLE, j_down : self.RUN, l_down : self.RUN, u_down : self.ATTACK},
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
class Jondahl_Attack:
    def __init__(self, jondahl):
        self.Jondahl = jondahl

    def enter(self, e):
        # keyup이 아닌 keydown으로 방향을 결정해야 함
        if l_down(e):
            self.Jondahl.dir = self.Jondahl.face_dir = 1
        elif j_down(e):
            self.Jondahl.dir = self.Jondahl.face_dir = -1

    def exit(self, e):
        self.Jondahl.frameX = 0
        pass

    def do(self):
        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.Jondahl.frames_per_animation.get('Jondahl_Attack', 1)

        self.Jondahl.TIME_PER_ACTION = 0.3
        self.Jondahl.ACTION_PER_TIME = 1.0 / self.Jondahl.TIME_PER_ACTION

        increment = length * self.Jondahl.ACTION_PER_TIME * game_framework.frame_time
        self.Jondahl.frameX = (self.Jondahl.frameX + increment) % length

        if self.Jondahl.frameX >= length - 1:
            self.Jondahl.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.Jondahl.images['Jondahl_Attack'][int(self.Jondahl.frameX)]
        draw_y = 0 + img.h / 2
        draw_x = self.Jondahl.x
        if self.Jondahl.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

class Jondahl_Run:
    def __init__(self, jondahl):
        self.Jondahl = jondahl

    def enter(self, e):
        # keyup이 아닌 keydown으로 방향을 결정해야 함
        if l_down(e):
            self.Jondahl.dir = self.Jondahl.face_dir = 1
        elif j_down(e):
            self.Jondahl.dir = self.Jondahl.face_dir = -1

    def exit(self, e):
        self.Jondahl.frameX = 0
        pass

    def do(self):
        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.Jondahl.frames_per_animation.get('Jondahl_Run', 1)

        self.Jondahl.TIME_PER_ACTION = 1.0
        self.Jondahl.ACTION_PER_TIME = 1.0 / self.Jondahl.TIME_PER_ACTION

        increment = length * self.Jondahl.ACTION_PER_TIME * game_framework.frame_time
        self.Jondahl.frameX = (self.Jondahl.frameX + increment) % length

        self.Jondahl.x += self.Jondahl.dir * RUN_SPEED_PPS * game_framework.frame_time

        img = self.Jondahl.images['Jondahl_Run'][int(self.Jondahl.frameX)]
        if self.Jondahl.x < img.w / 2:
            self.Jondahl.x = img.w / 2
        elif self.Jondahl.x > 1280 - img.w / 2:
            self.Jondahl.x = 1280 - img.w / 2

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
        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.Jondahl.frames_per_animation.get('Jondahl_Idle', 1)

        self.Jondahl.TIME_PER_ACTION = 2.0
        self.Jondahl.ACTION_PER_TIME = 1.0 / self.Jondahl.TIME_PER_ACTION

        increment = length * self.Jondahl.ACTION_PER_TIME * game_framework.frame_time
        self.Jondahl.frameX = (self.Jondahl.frameX + increment) % length
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
        self.x, self.y = 1280 - 97, 50
        self.frameX = 0
        self.frameY = 0
        self.face_dir = -1
        self.dir = -1
        self.animation_names = ['Jondahl_Idle', 'Jondahl_Run', 'Jondahl_Attack']
        self.images = {}
        self.render_size = {}
        self.TIME_PER_ACTION = 2.0
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        # per-animation frame count 저장
        self.frames_per_animation = {}
        for name in self.animation_names:
            if name == 'Jondahl_Idle':
                frames = [load_image("./Jondahl/" + name + " (%d)" % i + ".png") for i in range(1, 23)]
            elif name == 'Jondahl_Run':
                frames = [load_image("./Jondahl/" + name + " (%d)" % i + ".png") for i in range(1, 18)]
            elif name == 'Jondahl_Attack':
                frames = [load_image("./Jondahl/" + name + " (%d)" % i + ".png") for i in range(1, 5)]
            self.images[name] = frames
            max_w = max(img.w for img in frames)
            max_h = max(img.h for img in frames)
            self.render_size[name] = (max_w, max_h)
            self.frames_per_animation[name] = len(frames)

        self.IDLE = Jondahl_Idle(self)
        self.RUN = Jondahl_Run(self)
        self.ATTACK = Jondahl_Attack(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {i_down: self.IDLE, k_down: self.IDLE, j_down : self.RUN, l_down :self.RUN, u_down : self.ATTACK},
                self.RUN : {l_up : self.IDLE, j_up : self.IDLE, j_down : self.RUN, l_down : self.RUN, u_down : self.ATTACK},
                self.ATTACK : {time_out : self.IDLE, j_down : self.RUN, l_down : self.RUN, u_down : self.ATTACK},
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
class Zizou_Olympia_Attack:

    def __init__(self, zizou_Olympia):
        self.Zizou_Olympia = zizou_Olympia
        # 공격 지속시간(초)
        self.duration = 0.2
        self.elapsed = 0.0

    def enter(self, e):
        # 방향 결정
        if l_down(e):
            self.Zizou_Olympia.dir = self.Zizou_Olympia.face_dir = 1
        elif j_down(e):
            self.Zizou_Olympia.dir = self.Zizou_Olympia.face_dir = -1

        # 타이머 및 프레임 초기화
        self.elapsed = 0.0
        try:
            self.Zizou_Olympia.frameX = 0
        except Exception:
            pass
        if u_down(e):
            self.Zizou_Olympia.nomal_attack()
    def exit(self, e):
        # 정리
        try:
            self.Zizou_Olympia.frameX = 0
        except Exception:
            pass
        self.elapsed = 0.0

    def do(self):
        # 프레임 기반 애니메이션이 없고 이미지가 하나인 경우, 시간 누적으로 전환 처리
        self.elapsed += game_framework.frame_time
        if self.elapsed >= self.duration:
            self.Zizou_Olympia.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        # 단일 이미지(프레임 수 1) 안전하게 그리기
        imgs = self.Zizou_Olympia.images.get('Zizou Olympia_Attack')
        if not imgs:
            return
        img = imgs[0]
        draw_y = 0 + img.h / 2
        draw_x = self.Zizou_Olympia.x
        if self.Zizou_Olympia.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

class Zizou_Olympia_Run:

    def __init__(self, zizou_Olympia):
        self.Zizou_Olympia = zizou_Olympia

    def enter(self, e):
        # keyup이 아닌 keydown으로 방향을 결정해야 함
        if l_down(e):
            self.Zizou_Olympia.dir = self.Zizou_Olympia.face_dir = 1
        elif j_down(e):
            self.Zizou_Olympia.dir = self.Zizou_Olympia.face_dir = -1

    def exit(self, e):
        self.Zizou_Olympia.frameX = 0
        pass

    def do(self):
        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.Zizou_Olympia.frames_per_animation.get('Zizou Olympia_Run', 1)

        self.Zizou_Olympia.TIME_PER_ACTION = 1.0
        self.Zizou_Olympia.ACTION_PER_TIME = 1.0 / self.Zizou_Olympia.TIME_PER_ACTION

        increment = length * self.Zizou_Olympia.ACTION_PER_TIME * game_framework.frame_time
        self.Zizou_Olympia.frameX = (self.Zizou_Olympia.frameX + increment) % length

        # 이동 처리
        self.Zizou_Olympia.x += self.Zizou_Olympia.dir * RUN_SPEED_PPS * game_framework.frame_time

        img = self.Zizou_Olympia.images['Zizou Olympia_Run'][int(self.Zizou_Olympia.frameX)]
        if self.Zizou_Olympia.x < img.w / 2:
            self.Zizou_Olympia.x = img.w / 2
        elif self.Zizou_Olympia.x > 1280 - img.w / 2:
            self.Zizou_Olympia.x = 1280 - img.w / 2

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
        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.Zizou_Olympia.frames_per_animation.get('Zizou Olympia_Idle', 1)

        self.Zizou_Olympia.TIME_PER_ACTION = 2.0
        self.Zizou_Olympia.ACTION_PER_TIME = 1.0 / self.Zizou_Olympia.TIME_PER_ACTION

        increment = length * self.Zizou_Olympia.ACTION_PER_TIME * game_framework.frame_time
        self.Zizou_Olympia.frameX = (self.Zizou_Olympia.frameX + increment) % length

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
        self.x, self.y = 1280 - 97, 55
        self.frameX = 0
        self.frameY = 0
        self.face_dir = -1
        self.dir = -1
        self.animation_names = ['Zizou Olympia_Idle', 'Zizou Olympia_Run', 'Zizou Olympia_Attack']
        self.images = {}
        self.render_size = {}
        self.TIME_PER_ACTION = 2.0
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        # per-animation frame count 저장
        self.frames_per_animation = {}
        for name in self.animation_names:
            if name == 'Zizou Olympia_Idle':
                frames = [load_image("./Zizou_Olympia/" + name + " (%d)" % i + ".png") for i in range(1, 16)]
            elif name == 'Zizou Olympia_Run':
                frames = [load_image("./Zizou_Olympia/" + name + " (%d)" % i + ".png") for i in range(1, 7)]
            elif name == 'Zizou Olympia_Attack':
                frames = [load_image("./Zizou_Olympia/" + name + " (%d)" % i + ".png") for i in range(1, 2)]
            self.images[name] = frames
            max_w = max(img.w for img in frames)
            max_h = max(img.h for img in frames)
            self.render_size[name] = (max_w, max_h)
            self.frames_per_animation[name] = len(frames)

        self.IDLE = Zizou_Olympia_Idle(self)
        self.RUN = Zizou_Olympia_Run(self)
        self.ATTACK = Zizou_Olympia_Attack(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {i_down: self.IDLE, k_down: self.IDLE, j_down : self.RUN, l_down :self.RUN, u_down : self.ATTACK},
                self.RUN : {j_up : self.IDLE, l_up : self.IDLE, j_down : self.RUN, l_down : self.RUN, u_down : self.ATTACK},
                self.ATTACK : {time_out : self.IDLE, j_down : self.RUN, l_down : self.RUN, u_down : self.ATTACK},
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

    def nomal_attack(self):
        if self.face_dir < 0:
            olympia_attack = Olympia_attack(self.x + 60, self.y, self.face_dir)
            game_world.add_object(olympia_attack, 1)
        else:
            olympia_attack = Olympia_attack(self.x - 60, self.y, self.face_dir)
            game_world.add_object(olympia_attack, 1)



# 네 번째 캐릭터 구현
class Franzer_Attack:
    def __init__(self, franzer):
        self.Franzer = franzer

    def enter(self, e):
        # keyup이 아닌 keydown으로 방향을 결정해야 함
        if l_down(e):
            self.Franzer.dir = self.Franzer.face_dir = 1
        elif j_down(e):
            self.Franzer.dir = self.Franzer.face_dir = -1

    def exit(self, e):
        self.Franzer.frameX = 0
        pass

    def do(self):
        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.Franzer.frames_per_animation.get('Franzer_Attack', 1)

        self.Franzer.TIME_PER_ACTION = 0.3
        self.Franzer.ACTION_PER_TIME = 1.0 / self.Franzer.TIME_PER_ACTION

        increment = length * self.Franzer.ACTION_PER_TIME * game_framework.frame_time
        self.Franzer.frameX = (self.Franzer.frameX + increment) % length

        if self.Franzer.frameX >= length - 1:
            self.Franzer.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.Franzer.images['Franzer_Attack'][int(self.Franzer.frameX)]
        draw_y = 0 + img.h / 2
        draw_x = self.Franzer.x
        if self.Franzer.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

class Franzer_Run:

    def __init__(self, franzer):
        self.Franzer = franzer

    def enter(self, e):
        # keyup이 아닌 keydown으로 방향을 결정해야 함
        if l_down(e):
            self.Franzer.dir = self.Franzer.face_dir = 1
        elif j_down(e):
            self.Franzer.dir = self.Franzer.face_dir = -1

    def exit(self, e):
        self.Franzer.frameX = 0
        pass

    def do(self):
        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.Franzer.frames_per_animation.get('Franzer_Run', 1)

        self.Franzer.TIME_PER_ACTION = 1.0
        self.Franzer.ACTION_PER_TIME = 1.0 / self.Franzer.TIME_PER_ACTION

        increment = length * self.Franzer.ACTION_PER_TIME * game_framework.frame_time
        self.Franzer.frameX = (self.Franzer.frameX + increment) % length

        self.Franzer.x += self.Franzer.dir * RUN_SPEED_PPS * game_framework.frame_time

        img = self.Franzer.images['Franzer_Run'][int(self.Franzer.frameX)]
        if self.Franzer.x < img.w / 2:
            self.Franzer.x = img.w / 2
        elif self.Franzer.x > 1280 - img.w / 2:
            self.Franzer.x = 1280 - img.w / 2

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
        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.Franzer.frames_per_animation.get('Franzer_Idle', 1)

        self.Franzer.TIME_PER_ACTION = 2.0
        self.Franzer.ACTION_PER_TIME = 1.0 / self.Franzer.TIME_PER_ACTION

        increment = length * self.Franzer.ACTION_PER_TIME * game_framework.frame_time
        self.Franzer.frameX = (self.Franzer.frameX + increment) % length

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
        self.x, self.y = 1280 - 97, 50
        self.frameX = 0
        self.frameY = 0
        self.face_dir = -1
        self.dir = 1
        self.animation_names = ['Franzer_Idle', 'Franzer_Run', 'Franzer_Attack']
        self.images = {}
        # 각 애니메이션별로 최대 프레임 너비/높이를 저장하면 출력 크기를 통일하여 흔들림을 방지할 수 있음
        self.render_size = {}
        self.TIME_PER_ACTION = 2.0
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        # per-animation frame count 저장
        self.frames_per_animation = {}
        for name in self.animation_names:
            if name == 'Franzer_Idle':
                frames = [load_image("./Franzer/" + name + " (%d)" % i + ".png") for i in range(1, 4)]
            elif name == 'Franzer_Run':
                frames = [load_image("./Franzer/" + name + " (%d)" % i + ".png") for i in range(1, 7)]
            elif name == 'Franzer_Attack':
                frames = [load_image("./Franzer/" + name + " (%d)" % i + ".png") for i in range(1, 5)]
            self.images[name] = frames
            max_w = max(img.w for img in frames)
            max_h = max(img.h for img in frames)
            self.render_size[name] = (max_w, max_h)
            self.frames_per_animation[name] = len(frames)

        self.IDLE = Franzer_Idle(self)
        self.RUN = Franzer_Run(self)
        self.ATTACK = Franzer_Attack(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {i_down: self.IDLE, k_down: self.IDLE, j_down : self.RUN, l_down :self.RUN, u_down : self.ATTACK},
                self.RUN : {j_up : self.IDLE, l_up : self.IDLE, j_down : self.RUN, l_down : self.RUN, u_down : self.ATTACK},
                self.ATTACK : {time_out : self.IDLE, j_down : self.RUN, l_down : self.RUN, u_down : self.ATTACK},
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
