import pygame
import time
import math
from entities.entity import Entity


class Tower(Entity):

    def __init__(self, _pos: tuple, _symbol: pygame.image, _range, _cool_down):
        super().__init__(_pos, _symbol)
        self.range = _range
        self.timer = time.time()
        self.cool_down_time = _cool_down
        self.aimed_enemy = None
        self.active = False

    def is_in_range(self, pos):
        x1, y1 = pos
        x2, y2 = self.get_center()

        vector = (x2 - x1, y2 - y1)
        vector_length = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        if vector_length <= self.range:
            return True
        return False

    def set_aimed_enemy(self, enemy_list):
        """
        Traverses enemy list. First enemy within range will get aimed at.
        :param enemy_list:
        :return:
        """
        for enemy in enemy_list:
            if self.is_in_range(enemy.get_center()):
                self.active = True
                self.aimed_enemy = enemy
                break
            else:
                self.active = False
                self.aimed_enemy = None

    def draw_attack(self, win):
        if self.aimed_enemy is not None:
            pos = self.aimed_enemy.get_center()
            pygame.draw.line(win, (0, 0, 255), self.get_center(), pos, 2)
