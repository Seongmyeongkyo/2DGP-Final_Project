from pico2d import *
import game_world
import game_framework
import Hp_Ui

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Olympia_attack:
    image = None

    def __init__(self, x = 97, y = 70, face_dir = 1):
        if Olympia_attack.image == None:
            Olympia_attack.image = load_image("./Skill_impact/player1_Zizou_Olympia_attack.png")
        self.x, self.y = x, y
        self.face_dir = face_dir
        self.right_end_x = x + 200
        self.left_end_x = x - 200
        self.hit_objects = set()  # 이미 맞은 객체 추적 (중복 데미지 방지)

    def draw(self):
        if Olympia_attack.image and self.face_dir < 0:
            Olympia_attack.image.composite_draw(0, 'h', self.x, self.y)
        elif Olympia_attack.image and self.face_dir > 0:
            Olympia_attack.image.draw(self.x, self.y)

    def update(self):
        # 위치 업데이트
        self.x += RUN_SPEED_PPS * self.face_dir * game_framework.frame_time
        # 화면 밖으로 나가면 제거
        if self.face_dir < 0 and self.x < self.left_end_x:
            game_world.remove_object(self)
        elif self.face_dir > 0 and self.x > self.right_end_x:
            game_world.remove_object(self)
        elif self.x < 0 or self.x > 1280:
            game_world.remove_object(self)

    def get_bb(self):
        """충돌 박스 반환"""
        img = load_image("./Skill_impact/player1_Zizou_Olympia_attack.png")
        draw_x = self.x
        half_w = img.w / 2
        half_h = img.h / 2
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
                    obj.decrease_hp(10)
                    game_world.remove_object(self)
                    break

class Olympia_attack2:
    image = None

    def __init__(self, x = 1280-97, y = 70, face_dir = -1):
        if Olympia_attack2.image == None:
            Olympia_attack2.image = load_image("./Skill_impact/player1_Zizou_Olympia_attack.png")
        self.x, self.y = x, y
        self.face_dir = face_dir
        self.right_end_x = x + 200
        self.left_end_x = x - 200
        self.hit_objects = set() # 이미 맞은 객체 추적 (중복 데미지 방지)

    def draw(self):
        if Olympia_attack2.image and self.face_dir < 0:
            Olympia_attack2.image.composite_draw(0, 'h', self.x, self.y)
        elif Olympia_attack2.image and self.face_dir > 0:
            Olympia_attack2.image.draw(self.x, self.y)

    def update(self):
        self.x += RUN_SPEED_PPS * self.face_dir * game_framework.frame_time
        if self.face_dir < 0 and self.x < self.left_end_x:
            game_world.remove_object(self)
        elif self.face_dir > 0 and self.x > self.right_end_x:
            game_world.remove_object(self)
        elif self.x < 0 or self.x > 1280:
            game_world.remove_object(self)

    def get_bb(self):
        """충돌 박스 반환"""
        img = load_image("./Skill_impact/player1_Zizou_Olympia_attack.png")
        draw_x = self.x
        half_w = img.w / 2
        half_h = img.h / 2
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
                    obj.decrease_hp(10)
                    game_world.remove_object(self)
                    break

