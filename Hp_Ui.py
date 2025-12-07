from pico2d import *
import game_framework


class Player1_Hp_Ui:
    def __init__(self, minus_hp=0):
        self.image = load_image("./UI/HP bar.png")
        self.x = 300
        self.y = 720 - 50
        self.width = 400
        self.max_width = 400
        self.height = 30
        self.time = get_time()
    def update(self):
        pass

    def decrease_hp(self, amount):
        self.width -= amount
        if self.width <= 0:
            self.width = 0
        self.x = self.width / 2 + 100

    def draw(self):
        self.image.composite_draw(0, 'h', self.x, self.y, self.width, self.height)


class Player2_Hp_Ui:
    def __init__(self):
        self.image = load_image("./UI/Hp bar.png")
        self.x = 1280 - 300
        self.y = 720 - 50
        self.width = 400
        self.max_width = 400
        self.height = 30
        self.time = get_time()

    def update(self):
        pass

    def decrease_hp(self, amount):
        self.width -= amount
        if self.width <= 0:
            self.width = 0
        self.x = 1280 - (self.width / 2 + 100)

    def draw(self):
        self.image.composite_draw(0, 'h', self.x, self.y, self.width, self.height)