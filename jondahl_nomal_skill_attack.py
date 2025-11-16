from pico2d import *
import game_world
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Jondahl_Nomal_Skill_Attack:

    def __init__(self, x = 97, y = 70, face_dir = 1, counter = 2):
        self.frameX = 0
        self.animation_names = ['Jondahl_NomalSkill_Attack']
        self.images = {}
        # 각 애니메이션별로 최대 프레임 너비/높이를 저장하면 출력 크기를 통일하여 흔들림을 방지할 수 있음
        self.render_size = {}

        self.TIME_PER_ACTION = 0.3
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        # per-animation frame count 저장
        self.frames_per_animation = {}

        for name in self.animation_names:
            if name == 'Jondahl_NomalSkill_Attack':
                frames = [load_image("./Skill_impact/" + name + " (%d)" % i + ".png") for i in range(1, 9)]

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
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.images['Jondahl_NomalSkill_Attack'][int(self.frameX)]
        draw_x = self.x
        if self.face_dir < 0:
            img.composite_draw(0, 'h', draw_x, self.y, 222, 222)
        else:
            img.draw(draw_x, self.y, 222, 222)

    def update(self):
        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.frames_per_animation.get('Jondahl_NomalSkill_Attack', 1)

        self.TIME_PER_ACTION = 0.3
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION

        increment = length * self.ACTION_PER_TIME * game_framework.frame_time
        self.frameX = (self.frameX + increment)
        if not self.skill_triggered and int(self.frameX) == 4:
            if self.counter and self.counter > 0:
                new_x = self.x + (100 * self.face_dir)
                new_effect = Jondahl_Nomal_Skill_Attack(new_x, self.y, self.face_dir, self.counter - 1)
                game_world.add_object(new_effect, 1)
        if self.frameX >= length:
            game_world.remove_object(self)  # 마지막 프레임에서 제거
            self.skill_triggered = True
        # 화면 밖으로 나가면 제거
        if self.x < 0 or self.x > 1280:
            game_world.remove_object(self)



class Jondahl_Nomal_Skill_Attack2:
    def __init__(self, x = 1280 - 97, y = 70, face_dir = -1, counter = 2):
        self.frameX = 0
        self.animation_names = ['Jondahl_NomalSkill_Attack']
        self.images = {}
        # 각 애니메이션별로 최대 프레임 너비/높이를 저장하면 출력 크기를 통일하여 흔들림을 방지할 수 있음
        self.render_size = {}

        self.TIME_PER_ACTION = 0.3
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        # per-animation frame count 저장
        self.frames_per_animation = {}

        for name in self.animation_names:
            if name == 'Jondahl_NomalSkill_Attack':
                frames = [load_image("./Skill_impact/" + name + " (%d)" % i + ".png") for i in range(1, 9)]

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
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.images['Jondahl_NomalSkill_Attack'][int(self.frameX)]
        draw_x = self.x
        if self.face_dir < 0:
            img.composite_draw(0, 'h', draw_x, self.y, 222, 222)
        else:
            img.draw(draw_x, self.y, 222, 222)

    def update(self):
        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.frames_per_animation.get('Jondahl_NomalSkill_Attack', 1)

        self.TIME_PER_ACTION = 0.3
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION

        increment = length * self.ACTION_PER_TIME * game_framework.frame_time
        self.frameX = (self.frameX + increment)
        if not self.skill_triggered and int(self.frameX) == 4:
            if self.counter and self.counter > 0:
                new_x = self.x + (100 * self.face_dir)
                new_effect = Jondahl_Nomal_Skill_Attack(new_x, self.y, self.face_dir, self.counter - 1)
                game_world.add_object(new_effect, 1)
        if self.frameX >= length:
            game_world.remove_object(self)  # 마지막 프레임에서 제거
            self.skill_triggered = True
        # 화면 밖으로 나가면 제거
        if self.x < 0 or self.x > 1280:
            game_world.remove_object(self)