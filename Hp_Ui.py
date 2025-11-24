from pico2d import *

class Player1_Hp_Ui:
    def __init__(self):
        self.image = load_image("./UI/HP bar.png")
        self.x = 300
        self.y = 720 - 50
    def update(self):
        pass

    def draw(self):
        self.image.composite_draw(0, 'h', self.x, self.y, 400, 30)

class Player2_Hp_Ui:
    def __init__(self):
        self.image = load_image("./UI/Hp bar.png")
        self.x = 1280 - 300
        self.y = 720 - 50
    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 400, 30)
