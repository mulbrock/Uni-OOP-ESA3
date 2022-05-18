import pygame
import math
from entities.entity import Entity


class Projectile(Entity):

    def __init__(self, starting_pos, dest_pos, attack_power, level):
        self.level = level
        _symbol_path = "assets/img/projectiles/projectile_{}.png".format(level)
        super().__init__(starting_pos, _symbol_path)
        self.destination_pos = dest_pos
        self.impact_range = 60
        self.attack_power = attack_power
        self.impacted = False

    def get_destination(self):
        return self.destination_pos

    def draw_projectile(self, win):
        x1, y1 = self.get_center()
        x2, y2 = self.get_destination()

        dir_vector = ((x2 - x1) * 2, (y2 - y1) * 2)
        dir_vector_length = math.sqrt((dir_vector[0]) ** 2 + (dir_vector[1]) ** 2)
        dir_vector = (dir_vector[0] / dir_vector_length, dir_vector[1] / dir_vector_length)

        step = ((x1 + dir_vector[0]), (y1 + dir_vector[1]))

        self.set_center((step[0], step[1]))
        win.blit(self.get_symbol(), self.get_draw_pos())

        x1, y1 = self.get_center()

        if dir_vector[0] >= 0:
            if dir_vector[1] >= 0:
                if x1 >= x2 and y1 >= y2:
                    self.impacted = True
            else:
                if x1 >= x2 and y1 <= y2:
                    self.impacted = True
        else:
            if dir_vector[1] >= 0:
                if x1 <= x2 and y1 >= y2:
                    self.impacted = True
            else:
                if x1 <= x2 and y1 >= y2:
                    self.impacted = True

    def is_impacted(self):
        return self.impacted

    def is_in_impact_range(self, pos):
        x1, y1 = pos
        x2, y2 = self.get_center()

        vector = (x2 - x1, y2 - y1)
        vector_length = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        if vector_length <= self.impact_range:
            return True
        return False

    def handle_impact(self, enemy_list):
        for enemy in enemy_list:
            if self.is_in_impact_range(enemy.get_center()):
                enemy.lose_life(self.attack_power)

    def set_projectile_img_path(self, symbol_path):
        self.set_symbol_path(symbol_path)
