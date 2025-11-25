from pico2d import *
import game_world
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Franzer_Ultimate_Skill_Attack:

    def __init__(self, x = 97, y = 70, face_dir = 1, counter = 5):
        self.frameX = 0
        self.animation_names = ['Franzer_UltimateSkill_Attack']
        self.images = {}
        self.render_size = {}
        self.TIME_PER_ACTION = 0.3
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.frames_per_animation = {}

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
            if self.counter and self.counter > 0:
                new_x = self.x + (92 * self.face_dir)
                new_y = self.y
                new_effect = Franzer_Ultimate_Skill_Attack(new_x, new_y, self.face_dir, self.counter - 1)
                game_world.add_object(new_effect, 1)

        # if self.frameX >= length:
        #     self.skill_triggered = True
        #     return

        self.x += RUN_SPEED_PPS * self.face_dir * game_framework.frame_time
        if self.face_dir < 0:
            self.y += RUN_SPEED_PPS * self.face_dir * game_framework.frame_time
        else:
            self.y -= RUN_SPEED_PPS * self.face_dir * game_framework.frame_time

        # 이미지 높이를 얻어 화면 밖 판정에 사용
        img = self.images['Franzer_UltimateSkill_Attack'][int(min(self.frameX, length - 1))]

        # 화면 아래로 완전히 나가면 제거
        if self.y < 189:
            game_world.remove_object(self)

        # 화면 좌우 밖 판정 (원래 있던 로직 유지)
        if self.x < 0 or self.x > 1280:
            game_world.remove_object(self)



class Franzer_Ultimate_Skill_Attack2:
    def __init__(self, x = 1280 - 97, y = 70, face_dir = -1, counter = 5):
        self.frameX = 0
        self.animation_names = ['Franzer_UltimateSkill_Attack']
        self.images = {}
        self.render_size = {}
        self.TIME_PER_ACTION = 0.3
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.frames_per_animation = {}

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
            if self.counter and self.counter > 0:
                new_x = self.x + (92 * self.face_dir)
                new_y = self.y
                new_effect = Franzer_Ultimate_Skill_Attack(new_x, new_y, self.face_dir, self.counter - 1)
                game_world.add_object(new_effect, 1)

        # if self.frameX >= length:
        #     self.skill_triggered = True
        #     return

        self.x += RUN_SPEED_PPS * self.face_dir * game_framework.frame_time
        if self.face_dir < 0:
            self.y += RUN_SPEED_PPS * self.face_dir * game_framework.frame_time
        else:
            self.y -= RUN_SPEED_PPS * self.face_dir * game_framework.frame_time

        # 이미지 높이를 얻어 화면 밖 판정에 사용
        img = self.images['Franzer_UltimateSkill_Attack'][int(min(self.frameX, length - 1))]

        # 화면 아래로 완전히 나가면 제거
        if self.y < 189:
            game_world.remove_object(self)

        # 화면 좌우 밖 판정 (원래 있던 로직 유지)
        if self.x < 0 or self.x > 1280:
            game_world.remove_object(self)