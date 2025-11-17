from pico2d import *
import game_world
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 100.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Franzer_Cut_scene:
    image = None

    def __init__(self, x = 97, y = 70, face_dir = 1):
        self.x, self.y = x, y
        self.face_dir = face_dir
        self.duration = 4.0  # 컷신 지속 시간 (초)
        self.time = 0.0
    def init(self):
        if Franzer_Cut_scene.image == None:
            Franzer_Cut_scene.image = load_image("./Cutscene/Franzer_cutscene.png")
        self.x, self.y = -1024 / 2, 485

    def exit(self):
        pass

    def draw(self):
        clear_canvas()
        game_world.render()
        draw_rectangle(0, 0, 1280, 720, 0, 0, 0, 230, True)
        Franzer_Cut_scene.image.draw(self.x, self.y, 1024, 470)
        update_canvas()

    def update(self):
        # 위치 업데이트
        self.x += RUN_SPEED_PPS * self.face_dir * game_framework.frame_time
        # 화면 밖으로 나가면 제거
        if self.x >= 1024 / 2:
            self.x = 1024 / 2
            self.time += game_framework.frame_time * 12.0
            if self.time > self.duration:
                self.time = 0.0
                Franzer_Cut_scene.image = None
                game_framework.pop_mode()

    def finish(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass
    def handle_events(self, event = None):
        pass


class Franzer_Cut_scene2:
    image = None

    def __init__(self, x = 1280 - 97, y = 70, face_dir = -1):
        self.x, self.y = x, y
        self.face_dir = face_dir
        self.duration = 4.0  # 컷신 지속 시간 (초)
        self.time = 0.0
    def init(self):
        if Franzer_Cut_scene2.image == None:
            Franzer_Cut_scene2.image = load_image("./Cutscene/Franzer_cutscene.png")
        self.x, self.y = 1024 + (1024 / 2), 485

    def exit(self):
        pass

    def draw(self):
        clear_canvas()
        game_world.render()
        draw_rectangle(0, 0, 1280, 720, 0, 0, 0, 230, True)
        Franzer_Cut_scene2.image.composite_draw(0, 'h', self.x, self.y, 1024, 470)
        update_canvas()

    def update(self):
        # 위치 업데이트
        self.x += RUN_SPEED_PPS * self.face_dir * game_framework.frame_time
        # 화면 밖으로 나가면 제거
        if self.x <= 1024 - (1024 / 4):
            self.x = 1024 - (1024 / 4)
            self.time += game_framework.frame_time * 12.0
            if self.time > self.duration:
                self.time = 0.0
                Franzer_Cut_scene2.image = None
                game_framework.pop_mode()

    def finish(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass
    def handle_events(self, event = None):
        pass

