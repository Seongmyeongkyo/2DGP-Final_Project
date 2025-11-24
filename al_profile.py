from pico2d import *

class Al_profile:
    def __init__(self):
        self.image = load_image("./UI/Al_profile.png")
        self.x = 50
        self.y = 720 - 50
    def update(self):
        pass

    def draw(self):
        self.image.composite_draw(0, 'h', self.x, self.y, 100, 100)

class Al_profile2:
    def __init__(self):
        self.image = load_image("./UI/Al_profile.png")
        self.x = 1230
        self.y = 720 - 50
    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 100, 100)
