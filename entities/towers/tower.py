import pygame
import time
import math
from entities.entity import Entity


class Tower(Entity):

    def __init__(self, _pos: tuple, _symbol: pygame.image, _range, _cool_down, _attack_power, _cost):
        super().__init__(_pos, _symbol)

        self.build_cost = _cost

        self.range = _range
        self.range_upgrade_level = 0
        self.range_upgrade_cost = 1

        self.cool_down_time = _cool_down
        self.speed_upgrade_level = 0
        self.speed_upgrade_cost = 1

        self.attack_power = _attack_power
        self.attack_power_upgrade_level = 0
        self.attack_power_upgrade_cost = 1

        self.timer = time.time()
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
                return
        self.active = False
        self.aimed_enemy = None

    def draw_attack(self, win):
        raise NotImplementedError

    def attack(self):
        raise NotImplementedError

    def upgrade_range(self):
        self.range += 5
        self.range_upgrade_level += 1
        self.range_upgrade_cost += 2

    def get_upgrade_range_cost(self):
        return self.range_upgrade_cost

    def upgrade_power(self):
        self.attack_power += 1
        self.attack_power_upgrade_level += 1
        self.attack_power_upgrade_cost += 2

    def get_upgrade_power_cost(self):
        return self.attack_power_upgrade_cost

    def upgrade_speed(self):
        self.cool_down_time -= 0.01
        self.speed_upgrade_level += 1
        self.speed_upgrade_cost += 2

    def get_upgrade_cost(self):
        return self.speed_upgrade_cost

    def draw_range(self, win):
        pygame.draw.circle(win, [0, 200, 200, 50], self.get_center(), self.range, 2)
