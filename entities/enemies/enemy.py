import math
import pygame
from entities.entity import Entity


class Enemy(Entity):
    """
    Allgemeine Klasse. Hat keine Instanzen.
    """

    def __init__(self, _path, _hp, _symbol, _level):
        super().__init__(_path[0], _symbol)

        self.max_hp = _hp
        self.hp = _hp
        self.kill_reward = int(_level)

        self.path = _path
        self.path_stage = 0
        self.step_count = 0

        self.last_stage = len(self.path) - 1

    def move_forward(self):
        """
        Bewegt einen Enemy weiter vorwärts, abhängig von seiner aktuellen Position auf dem vordefinierten Pfad.
        :return: boolean: wenn bewegt -> True, wenn nicht -> False
        """
        x1, y1 = self.get_center()

        """Schaut, auf welchem Bereich des Pfades sich der Gegner befindet."""
        if self.path_stage + 1 < len(self.path):
            x2, y2 = self.path[self.path_stage + 1]
        else:
            return False

        """Vektorberechnung des Richtungsvektors"""
        dir_vector = ((x2 - x1) * 2, (y2 - y1) * 2)
        dir_vector_length = math.sqrt((dir_vector[0]) ** 2 +
                                      (dir_vector[1]) ** 2)
        dir_vector = (dir_vector[0] / dir_vector_length, dir_vector[1] /
                      dir_vector_length)

        step = ((x1 + dir_vector[0]), (y1 + dir_vector[1]))

        self.set_center((step[0], step[1]))
        x1, y1 = self.get_center()

        if dir_vector[0] >= 0:
            if dir_vector[1] >= 0:
                if x1 >= x2 and y1 >= y2:
                    self.path_stage += 1
            else:
                if x1 >= x2 and y1 <= y2:
                    self.path_stage += 1
        else:
            if dir_vector[1] >= 0:
                if x1 <= x2 and y1 >= y2:
                    self.path_stage += 1
            else:
                if x1 <= x2 and y1 >= y2:
                    self.path_stage += 1

        return True

    def draw_life(self, win):
        """
        Zeichnet den Health-Balken eines Gegners über seiner aktuellen Position.
        :param win: Das window, auf das es gezeichnet werden soll.
        :return:
        """
        life_ratio = self.hp / self.max_hp

        pygame.draw.rect(win, (255, 0, 0),
                         (self.get_draw_pos()[0] - 10,
                          self.get_draw_pos()[1] - 25, 40, 5), 0)
        pygame.draw.rect(win, (0, 255, 0),
                         (self.get_draw_pos()[0] - 10,
                          self.get_draw_pos()[1] - 25, 40 * life_ratio, 5), 0)

    def lose_life(self, amount):
        """
        Zieht dem Gegner Leben ab.
        :param amount: int
        :return:
        """
        self.hp -= amount

    def get_life(self):
        """
        Liefert das aktuelle Leben zurück.
        :return: int
        """
        return self.hp

    def increase_max_hp_by(self, hp):
        """
        Setzt den Wert des maximalen Lebens.
        :param hp: int
        :return:
        """
        self.hp = hp
        self.max_hp = hp
