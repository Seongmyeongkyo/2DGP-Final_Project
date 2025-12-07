from pico2d import *
import game_world
import game_framework
import Hp_Ui

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# 객체 바닥 충돌 위치 값 고정
Ground_y = 110

class Franzer_Ultimate_Skill_Attack:

    def __init__(self, x = 97, y = 70, face_dir = 1, counter = 5):
        self.frameX = 0
        self.animation_names = ['Franzer_UltimateSkill_Attack']
        self.images = {}
        self.render_size = {}
        self.TIME_PER_ACTION = 0.3
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.frames_per_animation = {}
        self.hit_objects = set()  # 이미 맞은 객체 추적 (중복 데미지 방지)
        for name in self.animation_names:
            if name == 'Franzer_UltimateSkill_Attack':
                frames = [load_image("./Skill_impact/" + name + " (%d)" % i + ".png") for i in range(1, 7)]

            self.images[name] = frames
            max_w = max(img.w for img in frames)
            max_h = max(img.h for img in frames)
            self.render_size[name] = (max_w, max_h)
            self.frames_per_animation[name] = len(frames)

        self.x, self.y = x, y
        self.face_dir = face_dir
        self.counter = counter
        self.skill_triggered = False

    def draw(self):
        img = self.images['Franzer_UltimateSkill_Attack'][int(min(self.frameX, self.frames_per_animation['Franzer_UltimateSkill_Attack'] - 1))]
        draw_x = self.x
        draw_y = self.y
        if self.face_dir < 0:
            img.composite_draw(45, 'h', draw_x, draw_y)

        else:
            img.composite_draw(-45, ' ', draw_x, draw_y)

    def update(self):
        length = self.frames_per_animation.get('Franzer_UltimateSkill_Attack', 1)

        self.TIME_PER_ACTION = 0.2
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION

        increment = length * self.ACTION_PER_TIME * game_framework.frame_time
        self.frameX = (self.frameX + increment)

        if not self.skill_triggered and int(self.frameX) == 3:
            self.skill_triggered = True
            if self.counter and self.counter > 0:
                new_x = self.x + (92 * self.face_dir)
                new_y = self.y
                new_effect = Franzer_Ultimate_Skill_Attack(new_x, new_y, self.face_dir, self.counter - 1)
                game_world.add_object(new_effect, 1)
                game_world.add_collision_pair('player1_skill:player2', new_effect, None)

        self.x += RUN_SPEED_PPS * self.face_dir * game_framework.frame_time
        if self.face_dir < 0:
            self.y += RUN_SPEED_PPS * self.face_dir * game_framework.frame_time
        else:
            self.y -= RUN_SPEED_PPS * self.face_dir * game_framework.frame_time

        # 이미지 높이를 얻어 화면 밖 판정에 사용
        img = self.images['Franzer_UltimateSkill_Attack'][int(min(self.frameX, length - 1))]

        bottom = self.y - img.h / 2
        # 화면 아래로 완전히 나가면 제거
        if bottom < Ground_y:
            game_world.remove_object(self)

        # 화면 좌우 밖 판정 (원래 있던 로직 유지)
        if self.x < 0 or self.x > 1280:
            game_world.remove_object(self)

    def get_bb(self):
        """충돌 박스 반환"""
        img = self.images['Franzer_UltimateSkill_Attack'][int(min(self.frameX, self.frames_per_animation['Franzer_UltimateSkill_Attack'] - 1))]
        draw_x = self.x
        half_w = img.w / 4
        half_h = img.h
        return draw_x - half_w, self.y - half_h, draw_x + half_w, self.y + half_h

    def handle_collision(self, group, other):
        if group == 'player1_skill:player2':
            # 이미 맞은 대상이면 무시
            if other in self.hit_objects:
                return

            self.hit_objects.add(other)

            # Player2의 HP 감소
            for obj in game_world.world[2]:
                if isinstance(obj, Hp_Ui.Player2_Hp_Ui):
                    obj.decrease_hp(20)
                    game_world.remove_object(self)
                    break



class Franzer_Ultimate_Skill_Attack2:
    def __init__(self, x = 1280 - 97, y = 70, face_dir = -1, counter = 5):
        self.frameX = 0
        self.animation_names = ['Franzer_UltimateSkill_Attack']
        self.images = {}
        self.render_size = {}
        self.TIME_PER_ACTION = 0.3
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.frames_per_animation = {}
        self.hit_objects = set()  # 이미 맞은 객체 추적 (중복 데미지 방지)
        for name in self.animation_names:
            if name == 'Franzer_UltimateSkill_Attack':
                frames = [load_image("./Skill_impact/" + name + " (%d)" % i + ".png") for i in range(1, 7)]

            self.images[name] = frames
            max_w = max(img.w for img in frames)
            max_h = max(img.h for img in frames)
            self.render_size[name] = (max_w, max_h)
            self.frames_per_animation[name] = len(frames)

        self.x, self.y = x, y
        self.face_dir = face_dir
        self.counter = counter
        self.skill_triggered = False

    def draw(self):
        img = self.images['Franzer_UltimateSkill_Attack'][
            int(min(self.frameX, self.frames_per_animation['Franzer_UltimateSkill_Attack'] - 1))]
        draw_x = self.x
        draw_y = self.y
        if self.face_dir < 0:
            img.composite_draw(45, 'h', draw_x, draw_y)

        else:
            img.composite_draw(-45, ' ', draw_x, draw_y)

    def update(self):
        length = self.frames_per_animation.get('Franzer_UltimateSkill_Attack', 1)

        self.TIME_PER_ACTION = 0.2
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION

        increment = length * self.ACTION_PER_TIME * game_framework.frame_time
        self.frameX = (self.frameX + increment)

        if not self.skill_triggered and int(self.frameX) == 3:
            self.skill_triggered = True
            if self.counter and self.counter > 0:
                new_x = self.x + (92 * self.face_dir)
                new_y = self.y
                new_effect = Franzer_Ultimate_Skill_Attack2(new_x, new_y, self.face_dir, self.counter - 1)
                game_world.add_object(new_effect, 1)
                game_world.add_collision_pair('player2_skill:player1', new_effect, None)

        self.x += RUN_SPEED_PPS * self.face_dir * game_framework.frame_time
        if self.face_dir < 0:
            self.y += RUN_SPEED_PPS * self.face_dir * game_framework.frame_time
        else:
            self.y -= RUN_SPEED_PPS * self.face_dir * game_framework.frame_time

        # 이미지 높이를 얻어 화면 밖 판정에 사용
        img = self.images['Franzer_UltimateSkill_Attack'][int(min(self.frameX, length - 1))]

        bottom = self.y - img.h / 2
        # 화면 아래로 완전히 나가면 제거
        if bottom < Ground_y:
            game_world.remove_object(self)

        # 화면 좌우 밖 판정 (원래 있던 로직 유지)
        if self.x < 0 or self.x > 1280:
            game_world.remove_object(self)

    def get_bb(self):
        """충돌 박스 반환"""
        img = self.images['Franzer_UltimateSkill_Attack'][int(min(self.frameX, self.frames_per_animation['Franzer_UltimateSkill_Attack'] - 1))]
        draw_x = self.x
        half_w = img.w / 4
        half_h = img.h
        return draw_x - half_w, self.y - half_h, draw_x + half_w, self.y + half_h

    def handle_collision(self, group, other):
        if group == 'player2_skill:player1':
            # 이미 맞은 대상이면 무시
            if other in self.hit_objects:
                return

            self.hit_objects.add(other)

            # Player1의 HP 감소
            for obj in game_world.world[2]:
                if isinstance(obj, Hp_Ui.Player1_Hp_Ui):
                    obj.decrease_hp(20)
                    game_world.remove_object(self)
                    break