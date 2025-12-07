from pico2d import *
import game_framework

class Player1_Mana_Ui:
    def __init__(self):
        self.image = load_image("./UI/mana bar.png")
        self.x = 175
        self.y = 720 - 75
        self.width = 150
        self.max_width = 150
        self.height = 20
        self.mana = 150  # 현재 마나
        self.max_mana = 150  # 최대 마나
        self.mana_regen_time = 0  # 마나 회복 타이머
        self.mana_regen_interval = 2.0  # 2초마다 회복
        self.mana_regen_amount = 10  # 10씩 회복

    def update(self):
        # 마나 자동 회복
        self.mana_regen_time += game_framework.frame_time
        if self.mana_regen_time >= self.mana_regen_interval:
            self.mana_regen_time = 0
            self.increase_mana(self.mana_regen_amount)
        self.x = 100 + self.width / 2  # x 위치 조정

    def decrease_mana(self, amount):
        self.mana -= amount
        if self.mana < 0:
            self.mana = 0
        # UI 너비 계산 (마나 비율에 따라)
        self.width = (self.mana / self.max_mana) * self.max_width

    def increase_mana(self, amount):
        self.mana += amount
        if self.mana > self.max_mana:
            self.mana = self.max_mana
        # UI 너비 계산
        self.width = (self.mana / self.max_mana) * self.max_width

    def set_mana(self, mana):
        self.mana = mana
        if self.mana > self.max_mana:
            self.mana = self.max_mana
        if self.mana < 0:
            self.mana = 0
        self.width = (self.mana / self.max_mana) * self.max_width

    def draw(self):
        self.image.composite_draw(0, 'h', self.x, self.y, self.width, self.height)


class Player2_Mana_Ui:
    def __init__(self):
        self.image = load_image("./UI/mana bar.png")
        self.x = 1280 - 175
        self.y = 720 - 75
        self.width = 150
        self.max_width = 150
        self.height = 20
        self.mana = 150  # 현재 마나
        self.max_mana = 150  # 최대 마나
        self.mana_regen_time = 0  # 마나 회복 타이머
        self.mana_regen_interval = 2.0  # 2초마다 회복
        self.mana_regen_amount = 10  # 10씩 회복

    def update(self):
        # 마나 자동 회복
        self.mana_regen_time += game_framework.frame_time
        if self.mana_regen_time >= self.mana_regen_interval:
            self.mana_regen_time = 0
            self.increase_mana(self.mana_regen_amount)
        self.x = 1280 - 100 - (self.width / 2)  # x 위치 조정

    def decrease_mana(self, amount):
        self.mana -= amount
        if self.mana < 0:
            self.mana = 0
        # UI 너비 계산 (마나 비율에 따라)
        self.width = (self.mana / self.max_mana) * self.max_width

    def increase_mana(self, amount):
        self.mana += amount
        if self.mana > self.max_mana:
            self.mana = self.max_mana
        # UI 너비 계산
        self.width = (self.mana / self.max_mana) * self.max_width

    def set_mana(self, mana):
        self.mana = mana
        if self.mana > self.max_mana:
            self.mana = self.max_mana
        if self.mana < 0:
            self.mana = 0
        self.width = (self.mana / self.max_mana) * self.max_width

    def draw(self):
        self.image.draw(self.x, self.y, self.width, self.height)