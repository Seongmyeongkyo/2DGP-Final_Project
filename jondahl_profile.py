from pico2d import *

class Jondahl_profile:
    def __init__(self, x=50, y=720 - 50, w=100, h=100):
        self.image = load_image("./UI/Jondahl_profile.png")
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def update(self):
        pass

    def draw(self):
        self.image.composite_draw(0, 'h', self.x, self.y, self.w, self.h)

class Jondahl_profile2:
    def __init__(self, x=1230, y=720 - 50, w=100, h=100):
        self.image = load_image("./UI/Jondahl_profile.png")
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, self.w, self.h)
