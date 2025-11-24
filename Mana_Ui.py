from pico2d import *

class Player1_Mana_Ui:
    def __init__(self):
        self.image = load_image("./UI/mana bar.png")
        self.x = 175
        self.y = 720 - 75
    def update(self):
        pass

    def draw(self):
        self.image.composite_draw(0, 'h', self.x, self.y, 150, 20)

class Player2_Mana_Ui:
    def __init__(self):
        self.image = load_image("./UI/mana bar.png")
        self.x = 1280 - 175
        self.y = 720 - 75
    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 150, 20)
