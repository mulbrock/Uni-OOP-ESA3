import pygame
import math
import time
from entities.towers.tower import Tower


class LaserTower(Tower):

    def __init__(self, pos: tuple):
        _symbol = pygame.image.load("assets/img/towers/laser_1.png")
        _range = 100
        _cool_down = 1.0
        super().__init__(pos, _symbol, _range, _cool_down)
        self.attack_power = 1

    def attack(self):
        if self.active:
            if time.time() - self.timer >= self.cool_down_time:
                self.timer = time.time()
                self.aimed_enemy.lose_life(self.attack_power)
                return True
        return False
