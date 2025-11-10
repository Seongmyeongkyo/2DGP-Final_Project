from pico2d import *
import game_world
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Al_Nomal_Skill_Attack:
    image = None

    def __init__(self, x = 97, y = 70, face_dir = 1):
        if Al_Nomal_Skill_Attack.image == None:
            Al_Nomal_Skill_Attack.image = load_image("./Skill_impact/Al_NomalSkill_Attack.png")
        self.x, self.y = x, y
        self.face_dir = face_dir
        self.right_end_x = x + 300
        self.left_end_x = x - 300

    def draw(self):
        if Al_Nomal_Skill_Attack.image and self.face_dir > 0:
            Al_Nomal_Skill_Attack.image.composite_draw(0, 'h', self.x, self.y, 123, 78)
        elif Al_Nomal_Skill_Attack.image and self.face_dir < 0:
            Al_Nomal_Skill_Attack.image.draw(self.x, self.y, 123, 78)

    def update(self):
        # 위치 업데이트
        self.x += RUN_SPEED_PPS * self.face_dir * game_framework.frame_time
        # 화면 밖으로 나가면 제거
        if self.face_dir < 0 and self.x < self.left_end_x:
            game_world.remove_object(self)
        elif self.face_dir > 0 and self.x > self.right_end_x:
            game_world.remove_object(self)
        if self.x < 0 or self.x > 1280:
            game_world.remove_object(self)