from pico2d import *
import game_world
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Al_Nomal_Skill_Attack:

    def __init__(self, x = 97, y = 70, face_dir = 1):
        self.frameX = 0
        self.animation_names = ['Al_NomalSkill_Attack']
        self.images = {}
        # 각 애니메이션별로 최대 프레임 너비/높이를 저장하면 출력 크기를 통일하여 흔들림을 방지할 수 있음
        self.render_size = {}

        self.TIME_PER_ACTION = 0.3
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        # per-animation frame count 저장
        self.frames_per_animation = {}

        for name in self.animation_names:
            if name == 'Al_NomalSkill_Attack':
                frames = [load_image("./Skill_impact/" + name + " (%d)" % i + ".png") for i in range(1, 9)]

            self.images[name] = frames
            max_w = max(img.w for img in frames)
            max_h = max(img.h for img in frames)
            self.render_size[name] = (max_w, max_h)
            self.frames_per_animation[name] = len(frames)

        self.x, self.y = x, y
        self.face_dir = face_dir
        self.right_end_x = x + 300
        self.left_end_x = x - 300

    def draw(self):
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.images['Al_NomalSkill_Attack'][int(self.frameX)]
        draw_x = self.x
        if self.face_dir < 0:
            img.composite_draw(0, 'h', draw_x, self.y, 190, 95)
        else:
            img.draw(draw_x, self.y, 190, 95)

    def update(self):
        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.frames_per_animation.get('Al_NomalSkill_Attack', 1)

        self.TIME_PER_ACTION = 0.5
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION

        increment = length * self.ACTION_PER_TIME * game_framework.frame_time
        self.frameX = (self.frameX + increment)
        if self.frameX >= length:
            self.frameX = length - 1  # 마지막 프레임에서 멈춤

        # 위치 업데이트
        self.x += RUN_SPEED_PPS * self.face_dir * game_framework.frame_time
        # 화면 밖으로 나가면 제거
        if self.face_dir < 0 and self.x < self.left_end_x:
            game_world.remove_object(self)
        elif self.face_dir > 0 and self.x > self.right_end_x:
            game_world.remove_object(self)
        if self.x < 0 or self.x > 1280:
            game_world.remove_object(self)

class Al_Nomal_Skill_Attack2:
    def __init__(self, x = 1280 - 97, y = 70, face_dir = -1):
        self.frameX = 0
        self.animation_names = ['Al_NomalSkill_Attack']
        self.images = {}
        # 각 애니메이션별로 최대 프레임 너비/높이를 저장하면 출력 크기를 통일하여 흔들림을 방지할 수 있음
        self.render_size = {}

        self.TIME_PER_ACTION = 0.3
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        # per-animation frame count 저장
        self.frames_per_animation = {}

        for name in self.animation_names:
            if name == 'Al_NomalSkill_Attack':
                frames = [load_image("./Skill_impact/" + name + " (%d)" % i + ".png") for i in range(1, 9)]

            self.images[name] = frames
            max_w = max(img.w for img in frames)
            max_h = max(img.h for img in frames)
            self.render_size[name] = (max_w, max_h)
            self.frames_per_animation[name] = len(frames)

        self.x, self.y = x, y
        self.face_dir = face_dir
        self.right_end_x = x + 300
        self.left_end_x = x - 300

    def draw(self):
        # 원본 크기로 중앙 정렬하여 그려 좌우 흔들림을 제거 (스케일링 없음)
        img = self.images['Al_NomalSkill_Attack'][int(self.frameX)]
        draw_x = self.x
        if self.face_dir < 0:
            img.composite_draw(0, 'h', draw_x, self.y, 190, 95)
        else:
            img.draw(draw_x, self.y, 190, 95)

    def update(self):
        # 애니메이션 길이와 프레임 타임을 소유자에서 가져와 계산
        length = self.frames_per_animation.get('Al_NomalSkill_Attack', 1)

        self.TIME_PER_ACTION = 0.5
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION

        increment = length * self.ACTION_PER_TIME * game_framework.frame_time
        self.frameX = (self.frameX + increment)
        if self.frameX >= length:
            self.frameX = length - 1  # 마지막 프레임에서 멈춤

        # 위치 업데이트
        self.x += RUN_SPEED_PPS * self.face_dir * game_framework.frame_time
        # 화면 밖으로 나가면 제거
        if self.face_dir < 0 and self.x < self.left_end_x:
            game_world.remove_object(self)
        elif self.face_dir > 0 and self.x > self.right_end_x:
            game_world.remove_object(self)
        if self.x < 0 or self.x > 1280:
            game_world.remove_object(self)