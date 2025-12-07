from pico2d import *

from state_machine import StateMachine
import game_world
import game_framework

# 캐릭터 스킬 및 일반공격 발사체 임포트
from olympia_attack import Olympia_attack2

from al_nomal_skill_attack import Al_Nomal_Skill_Attack2
from jondahl_nomal_skill_attack import Jondahl_Nomal_Skill_Attack2
from zizou_olympia_nomal_skill_attack import Zizou_Olympia_Nomal_Skill_Attack2

from al_ultimate_skill_attack import Al_Ultimate_Skill_Attack2
from franzer_ultimate_skill_attack import Franzer_Ultimate_Skill_Attack2

# 캐릭터 컷신 임포트
from al_cut_scene import Al_Cut_scene2
from jondahl_cut_scene import Jondahl_Cut_scene2
from zizou_olympia_cut_scene import Zizou_Olympia_Cut_scene2
from franzer_cut_scene import Franzer_Cut_scene2

# 캐릭터 프로필 이미지 임포트
from al_profile import Al_profile2
from jondahl_profile import Jondahl_profile2
from zizou_olympia_profile import Zizou_Olympia_profile2
from franzer_profile import Franzer_profile2

import Hp_Ui
import time
import Mana_Ui

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
def o_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_o
def p_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_p

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

FRANZER_PIXEL_PER_METER = (10.0 / 0.1)
FRANZER_RUN_SPEED_KMPH = 100.0  # Km / Hour
FRANZER_RUN_SPEED_MPM = (FRANZER_RUN_SPEED_KMPH * 1000.0 / 60.0)
FRANZER_RUN_SPEED_MPS = (FRANZER_RUN_SPEED_MPM / 60.0)
FRANZER_RUN_SPEED_PPS = (FRANZER_RUN_SPEED_MPS * FRANZER_PIXEL_PER_METER)

# 첫 번째 캐릭터 구현
class Al_UltimateSkill:

    def __init__(self, al):
        self.Al = al

    def enter(self, e):
        if l_down(e):
            self.Al.dir = self.Al.face_dir = 1
        elif j_down(e):
            self.Al.dir = self.Al.face_dir = -1
        if p_down(e):
            game_framework.push_mode(Al_Cut_scene2(self.Al.x, self.Al.y, -1))

        # 스킬 임펙트 생성 플래그
        self.Al.skill_triggered = False

    def exit(self, e):
        self.Al.frameX = 0
        self.Al.skill_triggered = False
        self.Al.ultimate_skill_used = True
        pass

    def do(self):

        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.Al.frames_per_animation.get('Al_UltimateSkill', 1)

        self.Al.TIME_PER_ACTION = 2.0
        self.Al.ACTION_PER_TIME = 1.0 / self.Al.TIME_PER_ACTION

        increment = length * self.Al.ACTION_PER_TIME * game_framework.frame_time
        self.Al.frameX = (self.Al.frameX + increment)

        # 스킬 임팩트 생성 시점에 한 번만 호출
        if not self.Al.skill_triggered and int(self.Al.frameX) == 10:
            self.Al.ultimateSkill_attack()
            self.Al.skill_triggered = True

        if self.Al.frameX >= length:
            self.Al.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.Al.images['Al_UltimateSkill'][int(self.Al.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Al.x
        if self.Al.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

    def get_bb(self):
        img = self.Al.images['Al_UltimateSkill'][int(self.Al.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Al.x
        half_w = img.w // 2
        half_h = img.h // 2
        return draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h


class Al_NomalSkill:

    def __init__(self, al):
        self.Al = al

    def enter(self, e):
        if l_down(e):
            self.Al.dir = self.Al.face_dir = 1
        elif j_down(e):
            self.Al.dir = self.Al.face_dir = -1
        if o_down(e) and self.Al.mana >= 50:
            self.Al.nomalSkill_attack()

    def exit(self, e):
        self.Al.frameX = 0
        if self.Al.mana >= 50:
            self.Al.mana -= 50
            # Mana UI 업데이트
            for obj in game_world.world[2]:
                if isinstance(obj, Mana_Ui.Player2_Mana_Ui):
                    obj.decrease_mana(50)
                    break

    def do(self):
        if self.Al.mana < 50:
            self.Al.state_machine.handle_state_event(('TIMEOUT', None))
            return
        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.Al.frames_per_animation.get('Al_NomalSkill', 1)

        self.Al.TIME_PER_ACTION = 0.3
        self.Al.ACTION_PER_TIME = 1.0 / self.Al.TIME_PER_ACTION

        increment = length * self.Al.ACTION_PER_TIME * game_framework.frame_time
        self.Al.frameX = (self.Al.frameX + increment)

        if self.Al.frameX >= length:
            self.Al.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.Al.images['Al_NomalSkill'][int(self.Al.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Al.x
        if self.Al.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

    def get_bb(self):
        img = self.Al.images['Al_NomalSkill'][int(self.Al.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Al.x
        half_w = img.w / 2
        half_h = img.h / 2
        return draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h

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
        self.Al.frameX = (self.Al.frameX + increment)

        if self.Al.frameX >= length:
            self.Al.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.Al.images['Al_Attack'][int(self.Al.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Al.x
        if self.Al.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

    def get_bb(self):
        img = self.Al.images['Al_Attack'][int(self.Al.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Al.x
        half_w = img.w / 2
        half_h = img.h / 2
        return draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h

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
        draw_y = 100 + img.h / 2
        draw_x = self.Al.x
        if self.Al.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

    def get_bb(self):
        img = self.Al.images['Al_Run'][int(self.Al.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Al.x
        half_w = img.w / 2
        half_h = img.h / 2
        return draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h

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
        draw_y = 100 + img.h / 2
        draw_x = self.Al.x
        if self.Al.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

    def get_bb(self):
        img = self.Al.images['Al_Idle'][int(self.Al.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Al.x
        half_w = img.w / 2
        half_h = img.h / 2
        return draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h

class Al:
    def __init__(self):
        self.x, self.y = 1280-97, 125
        self.frameX = 0
        self.frameY = 0
        self.face_dir = -1
        self.dir = 1
        self.max_mana = 150
        self.mana = 150
        # 충돌 쿨다운 추가
        self.last_hit_time = 0
        self.hit_cooldown = 0.5  # 0.5초마다 한 번만 데미지
        self.ultimate_skill_used = False  # 궁극기 사용 여부
        self.animation_names = ['Al_Idle', 'Al_Run', 'Al_Attack', 'Al_NomalSkill', 'Al_UltimateSkill']
        self.images = {}
        # 각 애니메이션별로 최대 프레임 너비/높이를 저장하면 출력 크기를 통일하여 흔들림을 방지할 수 있음
        self.render_size = {}

        self.TIME_PER_ACTION = 2.0
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        # per-animation frame count 저장
        self.frames_per_animation = {}
        # 캐릭터 이미지 프로필 객체 생성
        self.al_profile = Al_profile2()

        for name in self.animation_names:
            if name == 'Al_Idle':
                frames = [load_image("./AL/" + name + " (%d)" % i + ".png") for i in range(1, 24)]
            elif name == 'Al_Run':
                frames = [load_image("./AL/" + name + " (%d)" % i + ".png") for i in range(1, 9)]
            elif name == 'Al_Attack':
                frames = [load_image("./AL/" + name + " (%d)" % i + ".png") for i in range(1, 6)]
            elif name == 'Al_NomalSkill':
                frames = [load_image("./AL/" + name + " (%d)" % i + ".png") for i in range(1, 5)]
            elif name == 'Al_UltimateSkill':
                frames = [load_image("./AL/" + name + " (%d)" % i + ".png") for i in range(1, 24)]
            self.images[name] = frames
            max_w = max(img.w for img in frames)
            max_h = max(img.h for img in frames)
            self.render_size[name] = (max_w, max_h)
            self.frames_per_animation[name] = len(frames)

        self.IDLE = Al_Idle(self)
        self.RUN = Al_Run(self)
        self.ATTACK = Al_Attack(self)
        self.NOMAL_SKILL = Al_NomalSkill(self)
        self.ULTIMATE_SKILL = Al_UltimateSkill(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {i_down: self.IDLE, k_down: self.IDLE, j_down : self.RUN, l_down :self.RUN, u_down : self.ATTACK, o_down : self.NOMAL_SKILL, p_down : self.ULTIMATE_SKILL},
                self.RUN : {l_up : self.IDLE, j_up : self.IDLE, j_down : self.RUN, l_down : self.RUN, u_down : self.ATTACK, o_down : self.NOMAL_SKILL, p_down : self.ULTIMATE_SKILL},
                self.ATTACK : {time_out : self.IDLE, j_down : self.RUN, l_down : self.RUN, u_down : self.ATTACK, o_down : self.NOMAL_SKILL, p_down : self.ULTIMATE_SKILL},
                self.NOMAL_SKILL : {time_out : self.IDLE},
                self.ULTIMATE_SKILL : {time_out : self.IDLE},
            }
        )

    def update(self):
        self.state_machine.update()
        # Mana UI와 동기화 (선택사항)
        for obj in game_world.world[2]:
            if isinstance(obj, Mana_Ui.Player2_Mana_Ui):
                # UI의 마나를 캐릭터의 마나로 동기화
                if obj.mana != self.mana:
                    self.mana = obj.mana
                break

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_p:
            if self.ultimate_skill_used:
                return
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_o:
                if self.mana < 50:
                    return  # 마나가 부족하면 무시
        # 들어온 외부 키입력 등을 상태 머신에 전달하기 위해서
        # 튜플화 시킨 후, 전달
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        game_world.add_object(self.al_profile, 2)

    def nomalSkill_attack(self):
        if self.face_dir > 0:
            al_nomal_skill_attack = Al_Nomal_Skill_Attack2(self.x + 160, self.y + self.y / 3, self.face_dir)
            game_world.add_object(al_nomal_skill_attack, 1)
            game_world.add_collision_pair('player2_skill:player1', al_nomal_skill_attack, None)
        else:
            al_nomal_skill_attack = Al_Nomal_Skill_Attack2(self.x - 160, self.y + self.y / 3, self.face_dir)
            game_world.add_object(al_nomal_skill_attack, 1)
            game_world.add_collision_pair('player2_skill:player1', al_nomal_skill_attack, None)

    def ultimateSkill_attack(self):
        if self.face_dir > 0:
            al_ultimate_skill_attack = Al_Ultimate_Skill_Attack2(self.x + 160, self.y, self.face_dir)
            game_world.add_object(al_ultimate_skill_attack, 1)
            game_world.add_collision_pair('player2_skill:player1', al_ultimate_skill_attack, None)
        else:
            al_ultimate_skill_attack = Al_Ultimate_Skill_Attack2(self.x - 160, self.y, self.face_dir)
            game_world.add_object(al_ultimate_skill_attack, 1)
            game_world.add_collision_pair('player2_skill:player1', al_ultimate_skill_attack, None)

    def get_bb(self):
        # 상태 머신에서 현재 상태 객체를 찾아서 위임 시도
        sm = getattr(self, 'state_machine', None)
        if sm:
            for attr in ('current_state', 'cur_state', 'state', 'now_state', 'current', '_state'):
                state_obj = getattr(sm, attr, None)
                if state_obj and hasattr(state_obj, 'get_bb'):
                    try:
                        return state_obj.get_bb()
                    except Exception:
                        pass
            # 상태 머신 내부에 있는 어떤 속성이라도 get_bb를 제공하면 사용
            for v in vars(sm).values():
                if hasattr(v, 'get_bb'):
                    try:
                        return v.get_bb()
                    except Exception:
                        pass

        # 폴백: 렌더 사이즈 정보가 있으면 그 크기를 사용
        for name in getattr(self, 'animation_names', []):
            size = self.render_size.get(name)
            if size:
                w, h = size
                half = w / 2
                return (self.x - half, 100, self.x + half, 100 + h)

        # 최종 폴백 박스
        return (self.x - 25, 100, self.x + 25, 140)

    def handle_collision(self, group, other):
        """충돌 처리"""
        if group == 'player1:player2':
            # 쿨다운 체크
            current_time = time.time()
            if current_time - self.last_hit_time < self.hit_cooldown:
                return  # 쿨다운 중이면 무시

            sm = getattr(self, 'state_machine', None)
            if sm and hasattr(sm, 'cur_state'):
                state_name = sm.cur_state.__class__.__name__

                if 'Attack' in state_name or 'Skill' in state_name:
                    # Player1의 HP 감소
                    for obj in game_world.world[2]:
                        if isinstance(obj, Hp_Ui.Player1_Hp_Ui):
                            damage = 10
                            if 'UltimateSkill' in state_name:
                                damage = 30
                            elif 'NomalSkill' in state_name:
                                damage = 20
                            obj.decrease_hp(damage)
                            self.last_hit_time = current_time  # 쿨다운 시작
                            break


# 두 번째 캐릭터 구현
class Jondahl_UltimateSkill:
    def __init__(self, jondahl):
        self.Jondahl = jondahl

    def enter(self, e):
        # keyup이 아닌 keydown으로 방향을 결정해야 함
        if l_down(e):
            self.Jondahl.dir = self.Jondahl.face_dir = 1
        elif j_down(e):
            self.Jondahl.dir = self.Jondahl.face_dir = -1
        if p_down(e):
            game_framework.push_mode(Jondahl_Cut_scene2(self.Jondahl.x, self.Jondahl.y, -1))

        # 스킬 임펙트 생성 플래그
        self.Jondahl.skill_triggered = False

    def exit(self, e):
        self.Jondahl.frameX = 0
        self.Jondahl.skill_triggered = False
        self.Jondahl.ultimate_skill_used = True
        pass

    def do(self):
        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.Jondahl.frames_per_animation.get('Jondahl_NomalSkill', 1)

        self.Jondahl.TIME_PER_ACTION = 1.0
        self.Jondahl.ACTION_PER_TIME = 1.0 / self.Jondahl.TIME_PER_ACTION

        increment = length * self.Jondahl.ACTION_PER_TIME * game_framework.frame_time
        self.Jondahl.frameX = (self.Jondahl.frameX + increment)

        # 스킬 임팩트 생성 시점에 한 번만 호출
        if not self.Jondahl.skill_triggered and int(self.Jondahl.frameX) == 9:
            self.Jondahl.nomalSkill_attack()
            self.Jondahl.skill_triggered = True

        if self.Jondahl.frameX >= length - 1:
            self.Jondahl.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.Jondahl.images['Jondahl_NomalSkill'][int(self.Jondahl.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Jondahl.x
        if self.Jondahl.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

    def get_bb(self):
        img = self.Jondahl.images['Jondahl_NomalSkill'][int(self.Jondahl.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Jondahl.x
        half_w = img.w / 2
        half_h = img.h / 2
        return draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h


class Jondahl_NomalSkill:
    def __init__(self, jondahl):
        self.Jondahl = jondahl

    def enter(self, e):
        # keyup이 아닌 keydown으로 방향을 결정해야 함
        if l_down(e):
            self.Jondahl.dir = self.Jondahl.face_dir = 1
        elif j_down(e):
            self.Jondahl.dir = self.Jondahl.face_dir = -1

        # 스킬 임펙트 생성 플래그
        self.Jondahl.skill_triggered = False

    def exit(self, e):
        self.Jondahl.frameX = 0
        self.Jondahl.skill_triggered = False
        if self.Jondahl.mana >= 50:
            self.Jondahl.mana -= 50
            # Mana UI 업데이트
            for obj in game_world.world[2]:
                if isinstance(obj, Mana_Ui.Player2_Mana_Ui):
                    obj.decrease_mana(50)
                    break
        pass

    def do(self):
        if self.Jondahl.mana < 50:
            self.Jondahl.state_machine.handle_state_event(('TIMEOUT', None))
            return
        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.Jondahl.frames_per_animation.get('Jondahl_NomalSkill', 1)

        self.Jondahl.TIME_PER_ACTION = 1.0
        self.Jondahl.ACTION_PER_TIME = 1.0 / self.Jondahl.TIME_PER_ACTION

        increment = length * self.Jondahl.ACTION_PER_TIME * game_framework.frame_time
        self.Jondahl.frameX = (self.Jondahl.frameX + increment)

        # 스킬 임팩트 생성 시점에 한 번만 호출
        if not self.Jondahl.skill_triggered and int(self.Jondahl.frameX) == 9:
            self.Jondahl.nomalSkill_attack()
            self.Jondahl.skill_triggered = True

        if self.Jondahl.frameX >= length - 1:
            self.Jondahl.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.Jondahl.images['Jondahl_NomalSkill'][int(self.Jondahl.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Jondahl.x
        if self.Jondahl.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

    def get_bb(self):
        img = self.Jondahl.images['Jondahl_NomalSkill'][int(self.Jondahl.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Jondahl.x
        half_w = img.w / 2
        half_h = img.h / 2
        return draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h

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
        self.Jondahl.frameX = (self.Jondahl.frameX + increment)

        if self.Jondahl.frameX >= length:
            self.Jondahl.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.Jondahl.images['Jondahl_Attack'][int(self.Jondahl.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Jondahl.x
        if self.Jondahl.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

    def get_bb(self):
        img = self.Jondahl.images['Jondahl_Attack'][int(self.Jondahl.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Jondahl.x
        half_w = img.w / 2
        half_h = img.h / 2
        return draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h

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
        draw_y = 100 + img.h / 2
        draw_x = self.Jondahl.x
        if self.Jondahl.face_dir < 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

    def get_bb(self):
        img = self.Jondahl.images['Jondahl_Run'][int(self.Jondahl.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Jondahl.x
        half_w = img.w / 2
        half_h = img.h / 2
        return draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h

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
        draw_y = 100 + img.h / 2
        draw_x = self.Jondahl.x
        if self.Jondahl.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

    def get_bb(self):
        img = self.Jondahl.images['Jondahl_Idle'][int(self.Jondahl.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Jondahl.x
        half_w = img.w / 2
        half_h = img.h / 2
        return draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h

class Jondahl:
    def __init__(self):
        self.x, self.y = 1280 - 97, 150
        self.frameX = 0
        self.frameY = 0
        self.face_dir = -1
        self.dir = -1
        self.max_mana = 150
        self.mana = 150
        # 충돌 쿨다운 추가
        self.last_hit_time = 0
        self.hit_cooldown = 0.5  # 0.5초마다 한 번만 데미지
        self.ultimate_skill_used = False  # 궁극기 사용 여부
        self.animation_names = ['Jondahl_Idle', 'Jondahl_Run', 'Jondahl_Attack', 'Jondahl_NomalSkill']
        self.images = {}
        self.render_size = {}
        self.TIME_PER_ACTION = 2.0
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        # per-animation frame count 저장
        self.frames_per_animation = {}
        # 캐릭터 이미지 프로필 객체 생성
        self.jondahl_profile = Jondahl_profile2()

        for name in self.animation_names:
            if name == 'Jondahl_Idle':
                frames = [load_image("./Jondahl/" + name + " (%d)" % i + ".png") for i in range(1, 23)]
            elif name == 'Jondahl_Run':
                frames = [load_image("./Jondahl/" + name + " (%d)" % i + ".png") for i in range(1, 18)]
            elif name == 'Jondahl_Attack':
                frames = [load_image("./Jondahl/" + name + " (%d)" % i + ".png") for i in range(1, 5)]
            elif name == 'Jondahl_NomalSkill':
                frames = [load_image("./Jondahl/" + name + " (%d)" % i + ".png") for i in range(1, 13)]
            self.images[name] = frames
            max_w = max(img.w for img in frames)
            max_h = max(img.h for img in frames)
            self.render_size[name] = (max_w, max_h)
            self.frames_per_animation[name] = len(frames)

        self.IDLE = Jondahl_Idle(self)
        self.RUN = Jondahl_Run(self)
        self.ATTACK = Jondahl_Attack(self)
        self.NOMAL_SKILL = Jondahl_NomalSkill(self)
        self.ULTIMATE_SKILL = Jondahl_UltimateSkill(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {i_down: self.IDLE, k_down: self.IDLE, j_down : self.RUN, l_down :self.RUN, u_down : self.ATTACK, o_down : self.NOMAL_SKILL, p_down : self.ULTIMATE_SKILL},
                self.RUN : {l_up : self.IDLE, j_up : self.IDLE, j_down : self.RUN, l_down : self.RUN, u_down : self.ATTACK, o_down : self.NOMAL_SKILL, p_down : self.ULTIMATE_SKILL},
                self.ATTACK : {time_out : self.IDLE, j_down : self.RUN, l_down : self.RUN, u_down : self.ATTACK, o_down : self.NOMAL_SKILL, p_down : self.ULTIMATE_SKILL},
                self.NOMAL_SKILL : {time_out : self.IDLE},
                self.ULTIMATE_SKILL : {time_out : self.IDLE},
            }
        )

    def update(self):
        self.state_machine.update()
        # Mana UI와 동기화
        for obj in game_world.world[2]:
            if isinstance(obj, Mana_Ui.Player2_Mana_Ui):
                if obj.mana != self.mana:
                    self.mana = obj.mana
                break

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_p:
            if self.ultimate_skill_used:
                return
        # 들어온 외부 키입력 등을 상태 머신에 전달하기 위해서
        # 튜플화 시킨 후, 전달
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        game_world.add_object(self.jondahl_profile, 2)

    def nomalSkill_attack(self):
        if self.face_dir > 0:
            jondahl_nomal_skill_attack = Jondahl_Nomal_Skill_Attack2(self.x + 222, self.y + 40, self.face_dir)
            game_world.add_object(jondahl_nomal_skill_attack, 1)
            game_world.add_collision_pair('player2_skill:player1', jondahl_nomal_skill_attack, None)
        else:
            jondahl_nomal_skill_attack = Jondahl_Nomal_Skill_Attack2(self.x - 222, self.y + 40, self.face_dir)
            game_world.add_object(jondahl_nomal_skill_attack, 1)
            game_world.add_collision_pair('player2_skill:player1', jondahl_nomal_skill_attack, None)

    def get_bb(self):
        # 상태 머신에서 현재 상태 객체를 찾아서 위임 시도
        sm = getattr(self, 'state_machine', None)
        if sm:
            for attr in ('current_state', 'cur_state', 'state', 'now_state', 'current', '_state'):
                state_obj = getattr(sm, attr, None)
                if state_obj and hasattr(state_obj, 'get_bb'):
                    try:
                        return state_obj.get_bb()
                    except Exception:
                        pass
            # 상태 머신 내부에 있는 어떤 속성이라도 get_bb를 제공하면 사용
            for v in vars(sm).values():
                if hasattr(v, 'get_bb'):
                    try:
                        return v.get_bb()
                    except Exception:
                        pass

        # 폴백: 렌더 사이즈 정보가 있으면 그 크기를 사용
        for name in getattr(self, 'animation_names', []):
            size = self.render_size.get(name)
            if size:
                w, h = size
                half = w / 2
                return (self.x - half, 100, self.x + half, 100 + h)

        # 최종 폴백 박스
        return (self.x - 25, 100, self.x + 25, 140)

    def handle_collision(self, group, other):
        """충돌 처리"""
        if group == 'player1:player2':
            # 쿨다운 체크
            current_time = time.time()
            if current_time - self.last_hit_time < self.hit_cooldown:
                return  # 쿨다운 중이면 무시

            sm = getattr(self, 'state_machine', None)
            if sm and hasattr(sm, 'cur_state'):
                state_name = sm.cur_state.__class__.__name__

                if 'Attack' in state_name or 'Skill' in state_name:
                    # Player1의 HP 감소
                    for obj in game_world.world[2]:
                        if isinstance(obj, Hp_Ui.Player1_Hp_Ui):
                            damage = 10
                            if 'UltimateSkill' in state_name:
                                damage = 30
                            elif 'NomalSkill' in state_name:
                                damage = 20
                            obj.decrease_hp(damage)
                            self.last_hit_time = current_time  # 쿨다운 시작
                            break


# 세 번째 캐릭터 구현
class Zizou_Olympia_UltimateSkill:
    def __init__(self, zizou_Olympia):
        self.Zizou_Olympia = zizou_Olympia

    def enter(self, e):
        # keyup이 아닌 keydown으로 방향을 결정해야 함
        if l_down(e):
            self.Zizou_Olympia.dir = self.Zizou_Olympia.face_dir = 1
        elif j_down(e):
            self.Zizou_Olympia.dir = self.Zizou_Olympia.face_dir = -1
        if p_down(e):
            game_framework.push_mode(Zizou_Olympia_Cut_scene2(self.Zizou_Olympia.x, self.Zizou_Olympia.y, -1))

        # 스킬 임펙트 생성 플래그
        self.Zizou_Olympia.skill_triggered = False

    def exit(self, e):
        self.Zizou_Olympia.frameX = 0
        self.Zizou_Olympia.skill_triggered = False
        self.Zizou_Olympia.ultimate_skill_used = True
        pass

    def do(self):
        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.Zizou_Olympia.frames_per_animation.get('Zizou Olympia_NomalSkill', 1)

        self.Zizou_Olympia.TIME_PER_ACTION = 1.0
        self.Zizou_Olympia.ACTION_PER_TIME = 1.0 / self.Zizou_Olympia.TIME_PER_ACTION

        increment = length * self.Zizou_Olympia.ACTION_PER_TIME * game_framework.frame_time
        self.Zizou_Olympia.frameX = (self.Zizou_Olympia.frameX + increment)

        # 스킬 임팩트 생성 시점에 한 번만 호출
        if not self.Zizou_Olympia.skill_triggered and int(self.Zizou_Olympia.frameX) == 2:
            self.Zizou_Olympia.nomalSkill_attack()
            self.Zizou_Olympia.skill_triggered = True

        if self.Zizou_Olympia.frameX >= length:
            self.Zizou_Olympia.state_machine.handle_state_event(('TIMEOUT', None))


    def draw(self):
        # 화면 출력 시 바라보는 방향(face_dir)을 사용해서 멈춰있을 때도 올바른 뒤집기 유지
        img = self.Zizou_Olympia.images['Zizou Olympia_NomalSkill'][int(self.Zizou_Olympia.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Zizou_Olympia.x
        if self.Zizou_Olympia.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

    def get_bb(self):
        img = self.Zizou_Olympia.images['Zizou Olympia_NomalSkill'][int(self.Zizou_Olympia.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Zizou_Olympia.x
        half_w = img.w / 2
        half_h = img.h / 2
        return draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h


class Zizou_Olympia_NomalSkill:
    def __init__(self, zizou_Olympia):
        self.Zizou_Olympia = zizou_Olympia

    def enter(self, e):
        # keyup이 아닌 keydown으로 방향을 결정해야 함
        if l_down(e):
            self.Zizou_Olympia.dir = self.Zizou_Olympia.face_dir = 1
        elif j_down(e):
            self.Zizou_Olympia.dir = self.Zizou_Olympia.face_dir = -1

        # 스킬 임펙트 생성 플래그
        self.Zizou_Olympia.skill_triggered = False

    def exit(self, e):
        self.Zizou_Olympia.frameX = 0
        self.Zizou_Olympia.skill_triggered = False
        if self.Zizou_Olympia.mana >= 50:
            self.Zizou_Olympia.mana -= 50
            # Mana UI 업데이트
            for obj in game_world.world[2]:
                if isinstance(obj, Mana_Ui.Player2_Mana_Ui):
                    obj.decrease_mana(50)
                    break
        pass

    def do(self):
        if self.Zizou_Olympia.mana < 50:
            self.Zizou_Olympia.state_machine.handle_state_event(('TIMEOUT', None))
            return
        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.Zizou_Olympia.frames_per_animation.get('Zizou Olympia_NomalSkill', 1)

        self.Zizou_Olympia.TIME_PER_ACTION = 1.0
        self.Zizou_Olympia.ACTION_PER_TIME = 1.0 / self.Zizou_Olympia.TIME_PER_ACTION

        increment = length * self.Zizou_Olympia.ACTION_PER_TIME * game_framework.frame_time
        self.Zizou_Olympia.frameX = (self.Zizou_Olympia.frameX + increment)

        # 스킬 임팩트 생성 시점에 한 번만 호출
        if not self.Zizou_Olympia.skill_triggered and int(self.Zizou_Olympia.frameX) == 2:
            self.Zizou_Olympia.nomalSkill_attack()
            self.Zizou_Olympia.skill_triggered = True

        if self.Zizou_Olympia.frameX >= length:
            self.Zizou_Olympia.state_machine.handle_state_event(('TIMEOUT', None))


    def draw(self):
        # 화면 출력 시 바라보는 방향(face_dir)을 사용해서 멈춰있을 때도 올바른 뒤집기 유지
        img = self.Zizou_Olympia.images['Zizou Olympia_NomalSkill'][int(self.Zizou_Olympia.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Zizou_Olympia.x
        if self.Zizou_Olympia.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

    def get_bb(self):
        img = self.Zizou_Olympia.images['Zizou Olympia_NomalSkill'][int(self.Zizou_Olympia.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Zizou_Olympia.x
        half_w = img.w / 2
        half_h = img.h / 2
        return draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h

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
        draw_y = 100 + img.h / 2
        draw_x = self.Zizou_Olympia.x
        if self.Zizou_Olympia.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

    def get_bb(self):
        img = self.Zizou_Olympia.images['Zizou Olympia_Attack'][0]
        draw_y = 100 + img.h / 2
        draw_x = self.Zizou_Olympia.x
        half_w = img.w / 2
        half_h = img.h / 2
        return draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h

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
        draw_y = 100 + img.h / 2
        draw_x = self.Zizou_Olympia.x
        if self.Zizou_Olympia.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

    def get_bb(self):
        img = self.Zizou_Olympia.images['Zizou Olympia_Run'][int(self.Zizou_Olympia.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Zizou_Olympia.x
        half_w = img.w / 2
        half_h = img.h / 2
        return draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h

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
        draw_y = 100 + img.h / 2
        draw_x = self.Zizou_Olympia.x
        if self.Zizou_Olympia.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

    def get_bb(self):
        img = self.Zizou_Olympia.images['Zizou Olympia_Idle'][int(self.Zizou_Olympia.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Zizou_Olympia.x
        half_w = img.w / 2
        half_h = img.h / 2
        return draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h

class Zizou_Olympia:
    def __init__(self):
        self.x, self.y = 1280 - 97, 150
        self.frameX = 0
        self.frameY = 0
        self.face_dir = -1
        self.dir = -1
        self.max_mana = 150
        self.mana = 150
        # 충돌 쿨다운 추가
        self.last_hit_time = 0
        self.hit_cooldown = 0.5  # 0.5초마다 한 번만 데미지
        self.ultimate_skill_used = False  # 궁극기 사용 여부
        self.animation_names = ['Zizou Olympia_Idle', 'Zizou Olympia_Run', 'Zizou Olympia_Attack', 'Zizou Olympia_NomalSkill']
        self.images = {}
        self.render_size = {}
        self.TIME_PER_ACTION = 2.0
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        # per-animation frame count 저장
        self.frames_per_animation = {}
        # 캐릭터 프로필 이미지 객체 생성
        self.zizou_olympia_profile = Zizou_Olympia_profile2()
        for name in self.animation_names:
            if name == 'Zizou Olympia_Idle':
                frames = [load_image("./Zizou_Olympia/" + name + " (%d)" % i + ".png") for i in range(1, 16)]
            elif name == 'Zizou Olympia_Run':
                frames = [load_image("./Zizou_Olympia/" + name + " (%d)" % i + ".png") for i in range(1, 7)]
            elif name == 'Zizou Olympia_Attack':
                frames = [load_image("./Zizou_Olympia/" + name + " (%d)" % i + ".png") for i in range(1, 2)]
            elif name == 'Zizou Olympia_NomalSkill':
                frames = [load_image("./Zizou_Olympia/" + name + " (%d)" % i + ".png") for i in range(1, 4)]
            self.images[name] = frames
            max_w = max(img.w for img in frames)
            max_h = max(img.h for img in frames)
            self.render_size[name] = (max_w, max_h)
            self.frames_per_animation[name] = len(frames)

        self.IDLE = Zizou_Olympia_Idle(self)
        self.RUN = Zizou_Olympia_Run(self)
        self.ATTACK = Zizou_Olympia_Attack(self)
        self.NOMAL_SKILL = Zizou_Olympia_NomalSkill(self)
        self.ULTIMATE_SKILL = Zizou_Olympia_UltimateSkill(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {i_down: self.IDLE, k_down: self.IDLE, j_down : self.RUN, l_down :self.RUN, u_down : self.ATTACK, o_down : self.NOMAL_SKILL, p_down : self.ULTIMATE_SKILL},
                self.RUN : {j_up : self.IDLE, l_up : self.IDLE, j_down : self.RUN, l_down : self.RUN, u_down : self.ATTACK, o_down : self.NOMAL_SKILL, p_down : self.ULTIMATE_SKILL},
                self.ATTACK : {time_out : self.IDLE, j_down : self.RUN, l_down : self.RUN, u_down : self.ATTACK, o_down : self.NOMAL_SKILL, p_down : self.ULTIMATE_SKILL},
                self.NOMAL_SKILL : {time_out : self.IDLE},
                self.ULTIMATE_SKILL : {time_out : self.IDLE},
            }
        )

    def update(self):
        self.state_machine.update()
        # Mana UI와 동기화
        for obj in game_world.world[2]:
            if isinstance(obj, Mana_Ui.Player2_Mana_Ui):
                if obj.mana != self.mana:
                    self.mana = obj.mana
                break

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_p:
            if self.ultimate_skill_used:
                return
        # 들어온 외부 키입력 등을 상태 머신에 전달하기 위해서
        # 튜플화 시킨 후, 전달
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        game_world.add_object(self.zizou_olympia_profile, 2)

    def nomal_attack(self):
        if self.face_dir < 0:
            olympia_attack = Olympia_attack2(self.x - 60, self.y, self.face_dir)
            game_world.add_object(olympia_attack, 1)
            game_world.add_collision_pair('player2_skill:player1', olympia_attack, None)
        else:
            olympia_attack = Olympia_attack2(self.x + 60, self.y, self.face_dir)
            game_world.add_object(olympia_attack, 1)
            game_world.add_collision_pair('player2_skill:player1', olympia_attack, None)

    def nomalSkill_attack(self):
        if self.face_dir > 0:
            zizou_olympia_nomal_skill_attack = Zizou_Olympia_Nomal_Skill_Attack2(self.x + 36, self.y, self.face_dir)
            game_world.add_object(zizou_olympia_nomal_skill_attack, 1)
            game_world.add_collision_pair('player2_skill:player1', zizou_olympia_nomal_skill_attack, None)
        else:
            zizou_olympia_nomal_skill_attack = Zizou_Olympia_Nomal_Skill_Attack2(self.x - 36, self.y, self.face_dir)
            game_world.add_object(zizou_olympia_nomal_skill_attack, 1)
            game_world.add_collision_pair('player2_skill:player1', zizou_olympia_nomal_skill_attack, None)

    def get_bb(self):
        # 상태 머신에서 현재 상태 객체를 찾아서 위임 시도
        sm = getattr(self, 'state_machine', None)
        if sm:
            for attr in ('current_state', 'cur_state', 'state', 'now_state', 'current', '_state'):
                state_obj = getattr(sm, attr, None)
                if state_obj and hasattr(state_obj, 'get_bb'):
                    try:
                        return state_obj.get_bb()
                    except Exception:
                        pass
            # 상태 머신 내부에 있는 어떤 속성이라도 get_bb를 제공하면 사용
            for v in vars(sm).values():
                if hasattr(v, 'get_bb'):
                    try:
                        return v.get_bb()
                    except Exception:
                        pass

        # 폴백: 렌더 사이즈 정보가 있으면 그 크기를 사용
        for name in getattr(self, 'animation_names', []):
            size = self.render_size.get(name)
            if size:
                w, h = size
                half = w / 2
                return (self.x - half, 100, self.x + half, 100 + h)

        # 최종 폴백 박스
        return (self.x - 25, 100, self.x + 25, 140)

    def handle_collision(self, group, other):
        """충돌 처리"""
        if group == 'player1:player2':
            # 쿨다운 체크
            current_time = time.time()
            if current_time - self.last_hit_time < self.hit_cooldown:
                return  # 쿨다운 중이면 무시

            sm = getattr(self, 'state_machine', None)
            if sm and hasattr(sm, 'cur_state'):
                state_name = sm.cur_state.__class__.__name__

                if 'Attack' in state_name or 'Skill' in state_name:
                    # Player1의 HP 감소
                    for obj in game_world.world[2]:
                        if isinstance(obj, Hp_Ui.Player1_Hp_Ui):
                            damage = 10
                            if 'UltimateSkill' in state_name:
                                damage = 30
                            elif 'NomalSkill' in state_name:
                                damage = 20
                            obj.decrease_hp(damage)
                            self.last_hit_time = current_time  # 쿨다운 시작
                            break

# 네 번째 캐릭터 구현
class Franzer_UltimateSkill:
    def __init__(self, franzer):
        self.Franzer = franzer

    def enter(self, e):
        # keyup이 아닌 keydown으로 방향을 결정해야 함
        if l_down(e):
            self.Franzer.dir = self.Franzer.face_dir = 1
        elif j_down(e):
            self.Franzer.dir = self.Franzer.face_dir = -1
        if p_down(e):
            game_framework.push_mode(Franzer_Cut_scene2(self.Franzer.x, self.Franzer.y, -1))

        # 이동 플래그 생성
        self.Franzer.is_moving = True
        # 스킬 임펙트 생성 플래그
        self.Franzer.skill_triggered = False

    def exit(self, e):
        self.Franzer.frameX = 0
        self.Franzer.is_moving = True
        self.Franzer.skill_triggered = False
        self.Franzer.ultimate_skill_used = True
        pass

    def do(self):
        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.Franzer.frames_per_animation.get('Franzer_UltimateSkill', 1)
        self.Franzer.TIME_PER_ACTION = 1.5
        self.Franzer.ACTION_PER_TIME = 1.0 / self.Franzer.TIME_PER_ACTION

        increment = length * self.Franzer.ACTION_PER_TIME * game_framework.frame_time
        self.Franzer.frameX = (self.Franzer.frameX + increment)

        # 스킬 임팩트 생성 시점에 한 번만 호출
        if not self.Franzer.skill_triggered and int(self.Franzer.frameX) == 8:
            self.Franzer.ultimateSkill_attack()
            self.Franzer.skill_triggered = True

        if self.Franzer.frameX >= length:
            self.Franzer.state_machine.handle_state_event(('TIMEOUT', None))

        # 위치 업데이트
        if self.Franzer.is_moving and int(self.Franzer.frameX) == 8:
            self.Franzer.x += self.Franzer.face_dir * FRANZER_RUN_SPEED_PPS * game_framework.frame_time * 1.5
            if self.Franzer.x < 0:
                self.Franzer.x = 0
            elif self.Franzer.x > 1280:
                self.Franzer.x = 1280
            if self.Franzer.frameX >= length:
                self.Franzer.is_moving = False

    def draw(self):
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.Franzer.images['Franzer_UltimateSkill'][int(self.Franzer.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Franzer.x
        if self.Franzer.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

    def get_bb(self):
        img = self.Franzer.images['Franzer_UltimateSkill'][int(self.Franzer.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Franzer.x
        half_w = img.w / 2
        half_h = img.h / 2
        return draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h


class Franzer_NomalSkill:
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
        if self.Franzer.mana >= 50:
            self.Franzer.mana -= 50
            # Mana UI 업데이트
            for obj in game_world.world[2]:
                if isinstance(obj, Mana_Ui.Player2_Mana_Ui):
                    obj.decrease_mana(50)
                    break
        pass

    def do(self):
        if self.Franzer.mana < 50:
            self.Franzer.state_machine.handle_state_event(('TIMEOUT', None))
            return
        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.Franzer.frames_per_animation.get('Franzer_NomalSkill', 1)
        self.Franzer.TIME_PER_ACTION = 1.0
        self.Franzer.ACTION_PER_TIME = 1.0 / self.Franzer.TIME_PER_ACTION

        increment = length * self.Franzer.ACTION_PER_TIME * game_framework.frame_time
        self.Franzer.frameX = (self.Franzer.frameX + increment)

        if self.Franzer.frameX >= length:
            self.Franzer.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.Franzer.images['Franzer_NomalSkill'][int(self.Franzer.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Franzer.x
        if self.Franzer.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

    def get_bb(self):
        img = self.Franzer.images['Franzer_NomalSkill'][int(self.Franzer.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Franzer.x
        half_w = img.w / 2
        half_h = img.h / 2
        return draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h

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
        self.Franzer.frameX = (self.Franzer.frameX + increment)

        if self.Franzer.frameX >= length:
            self.Franzer.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.Franzer.images['Franzer_Attack'][int(self.Franzer.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Franzer.x
        if self.Franzer.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

    def get_bb(self):
        img = self.Franzer.images['Franzer_Attack'][int(self.Franzer.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Franzer.x
        half_w = img.w / 2
        half_h = img.h / 2
        return draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h

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
        draw_y = 100 + img.h / 2
        draw_x = self.Franzer.x
        if self.Franzer.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

    def get_bb(self):
        img = self.Franzer.images['Franzer_Run'][int(self.Franzer.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Franzer.x
        half_w = img.w / 2
        half_h = img.h / 2
        return draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h

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
        draw_y = 100 + img.h / 2
        draw_x = self.Franzer.x
        if self.Franzer.face_dir > 0:
            img.composite_draw(0, 'h', draw_x, draw_y)
        else:
            img.draw(draw_x, draw_y)

    def get_bb(self):
        img = self.Franzer.images['Franzer_Idle'][int(self.Franzer.frameX)]
        draw_y = 100 + img.h / 2
        draw_x = self.Franzer.x
        half_w = img.w / 2
        half_h = img.h / 2
        return draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h

class Franzer:
    def __init__(self):
        self.x, self.y = 1280 - 97, 100
        self.frameX = 0
        self.frameY = 0
        self.face_dir = -1
        self.dir = 1
        self.max_mana = 150
        self.mana = 150
        # 충돌 쿨다운 추가
        self.last_hit_time = 0
        self.hit_cooldown = 1.0
        self.ultimate_skill_used = False  # 궁극기 사용 여부
        self.animation_names = ['Franzer_Idle', 'Franzer_Run', 'Franzer_Attack', 'Franzer_NomalSkill', 'Franzer_UltimateSkill']
        self.images = {}
        # 각 애니메이션별로 최대 프레임 너비/높이를 저장하면 출력 크기를 통일하여 흔들림을 방지할 수 있음
        self.render_size = {}
        self.TIME_PER_ACTION = 2.0
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        # per-animation frame count 저장
        self.frames_per_animation = {}
        # 캐릭터 이미지 프로필 객체 생성
        self.franzer_profile = Franzer_profile2()
        for name in self.animation_names:
            if name == 'Franzer_Idle':
                frames = [load_image("./Franzer/" + name + " (%d)" % i + ".png") for i in range(1, 4)]
            elif name == 'Franzer_Run':
                frames = [load_image("./Franzer/" + name + " (%d)" % i + ".png") for i in range(1, 7)]
            elif name == 'Franzer_Attack':
                frames = [load_image("./Franzer/" + name + " (%d)" % i + ".png") for i in range(1, 5)]
            elif name == 'Franzer_NomalSkill':
                frames = [load_image("./Franzer/" + name + " (%d)" % i + ".png") for i in range(1, 11)]
            elif name == 'Franzer_UltimateSkill':
                frames = [load_image("./Franzer/" + name + " (%d)" % i + ".png") for i in range(1, 13)]
            self.images[name] = frames
            max_w = max(img.w for img in frames)
            max_h = max(img.h for img in frames)
            self.render_size[name] = (max_w, max_h)
            self.frames_per_animation[name] = len(frames)

        self.IDLE = Franzer_Idle(self)
        self.RUN = Franzer_Run(self)
        self.ATTACK = Franzer_Attack(self)
        self.NOMAL_SKILL = Franzer_NomalSkill(self)
        self.ULTIMATE_SKILL = Franzer_UltimateSkill(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {i_down: self.IDLE, k_down: self.IDLE, j_down : self.RUN, l_down :self.RUN, u_down : self.ATTACK, o_down : self.NOMAL_SKILL, p_down : self.ULTIMATE_SKILL},
                self.RUN : {j_up : self.IDLE, l_up : self.IDLE, j_down : self.RUN, l_down : self.RUN, u_down : self.ATTACK, o_down : self.NOMAL_SKILL, p_down : self.ULTIMATE_SKILL},
                self.ATTACK : {time_out : self.IDLE, j_down : self.RUN, l_down : self.RUN, u_down : self.ATTACK, o_down : self.NOMAL_SKILL, p_down : self.ULTIMATE_SKILL},
                self.NOMAL_SKILL : {time_out : self.IDLE},
                self.ULTIMATE_SKILL : {time_out : self.IDLE},
            }
        )

    def update(self):
        self.state_machine.update()
        # Mana UI와 동기화
        for obj in game_world.world[2]:
            if isinstance(obj, Mana_Ui.Player2_Mana_Ui):
                if obj.mana != self.mana:
                    self.mana = obj.mana
                break

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_p:
            if self.ultimate_skill_used:
                return
        # 들어온 외부 키입력 등을 상태 머신에 전달하기 위해서
        # 튜플화 시킨 후, 전달
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        game_world.add_object(self.franzer_profile, 2)

    def ultimateSkill_attack(self):
        if self.face_dir > 0:
            franzer_ultimate_skill_attack = Franzer_Ultimate_Skill_Attack2(self.x + 150, self.y + 250, self.face_dir)
            game_world.add_object(franzer_ultimate_skill_attack, 1)
            game_world.add_collision_pair('player2_skill:player1', franzer_ultimate_skill_attack, None)
        else:
            franzer_ultimate_skill_attack = Franzer_Ultimate_Skill_Attack2(self.x - 150, self.y + 250, self.face_dir)
            game_world.add_object(franzer_ultimate_skill_attack, 1)
            game_world.add_collision_pair('player2_skill:player1', franzer_ultimate_skill_attack, None)

    def get_bb(self):
        # 상태 머신에서 현재 상태 객체를 찾아서 위임 시도
        sm = getattr(self, 'state_machine', None)
        if sm:
            for attr in ('current_state', 'cur_state', 'state', 'now_state', 'current', '_state'):
                state_obj = getattr(sm, attr, None)
                if state_obj and hasattr(state_obj, 'get_bb'):
                    try:
                        return state_obj.get_bb()
                    except Exception:
                        pass
            # 상태 머신 내부에 있는 어떤 속성이라도 get_bb를 제공하면 사용
            for v in vars(sm).values():
                if hasattr(v, 'get_bb'):
                    try:
                        return v.get_bb()
                    except Exception:
                        pass

        # 폴백: 렌더 사이즈 정보가 있으면 그 크기를 사용
        for name in getattr(self, 'animation_names', []):
            size = self.render_size.get(name)
            if size:
                w, h = size
                half = w / 2
                return (self.x - half, 100, self.x + half, 100 + h)

        # 최종 폴백 박스
        return (self.x - 25, 100, self.x + 25, 140)

    def handle_collision(self, group, other):
        """충돌 처리"""
        if group == 'player1:player2':
            # 쿨다운 체크
            current_time = time.time()
            if current_time - self.last_hit_time < self.hit_cooldown:
                return  # 쿨다운 중이면 무시

            sm = getattr(self, 'state_machine', None)
            if sm and hasattr(sm, 'cur_state'):
                state_name = sm.cur_state.__class__.__name__

                if 'Attack' in state_name or 'Skill' in state_name:
                    # Player1의 HP 감소
                    for obj in game_world.world[2]:
                        if isinstance(obj, Hp_Ui.Player1_Hp_Ui):
                            damage = 10
                            if 'UltimateSkill' in state_name:
                                damage = 30
                            elif 'NomalSkill' in state_name:
                                damage = 20
                            obj.decrease_hp(damage)
                            self.last_hit_time = current_time  # 쿨다운 시작
                            break