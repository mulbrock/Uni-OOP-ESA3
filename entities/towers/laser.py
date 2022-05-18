import pygame
import time
from entities.towers.tower import Tower


class LaserTower(Tower):

    def __init__(self, pos: tuple):
        _symbol_path = "assets/img/towers/laser_1.png"
        _range = 100
        _cool_down = 0.5
        _attack_power = 0.5
        _cost = 4
        super().__init__(pos, _symbol_path, _range, _cool_down, _attack_power, _cost)

    def attack(self):
        if self.active:
            if time.time() - self.timer >= self.cool_down_time:
                self.timer = time.time()
                self.aimed_enemy.lose_life(self.attack_power)
                return True
        return False

    def draw_attack(self, win):
        if self.aimed_enemy is not None:
            pos = self.aimed_enemy.get_center()
            pygame.draw.line(win, (0, 0, 255), self.get_center(), pos, 2)
