import pygame
import time
import math
import re
from entities.entity import Entity


class Tower(Entity):

    def __init__(self, _pos: tuple, _symbol_path, _range, _cool_down, _attack_power,
                 _cost):
        super().__init__(_pos, _symbol_path)

        self.build_cost = _cost

        self.range = _range
        self.range_level = 1
        self.range_upgrade_cost = 1

        self.cool_down_time = _cool_down
        self.speed_level = 1
        self.speed_upgrade_cost = 1

        self.attack_power = _attack_power
        self.attack_power_level = 1
        self.attack_power_upgrade_cost = 1

        self.timer = time.time()
        self.aimed_enemy = None
        self.active = False

    def is_in_range(self, pos):
        """
        Überprüft, ob die eingegebene Position in Reichweite ist.
        :param pos:
        :return:
        """
        x1, y1 = pos
        x2, y2 = self.get_center()

        vector = (x2 - x1, y2 - y1)
        vector_length = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        if vector_length <= self.range:
            return True
        return False

    def set_aimed_enemy(self, enemy_list):
        """
        Durchläuft die eingegebene Liste mit Gegnern und visiert den ersten Gegner an, der in Reichweite ist.
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

    def upgrade_range(self):
        """
        Erhöht die Reichweite und die Kosten, für diese Reichweitenerhöhung.
        :return:
        """
        if self.range_level < 10:
            self.range_upgrade_cost += 4 * self.fibonacci(self.range_level)
            self.range += 5
            self.range_level += 1
            return True
        return False

    def get_upgrade_range_cost(self):
        """
        Gibt die aktuellen Kosten für ein Upgrade der Reichweite zurück.
        :return: einen integer-Wert der aktuellen Upgrade-Range-Kosten.
        """
        return self.range_upgrade_cost

    def upgrade_power(self):
        """
        Erhöht die Stärke und die Kosten, für diese Erhöhung.
        :return:
        """
        if self.attack_power_level < 10:
            self.attack_power_upgrade_cost += 4 * self.fibonacci(self.attack_power_level)
            self.attack_power += 1
            self.attack_power_level += 1
            self.update_symbol()
            return True
        return False

    def get_upgrade_power_cost(self):
        """
        Gibt die aktuellen Kosten für ein Power upgrade zurück.
        :return: int
        """
        return self.attack_power_upgrade_cost

    def upgrade_speed(self):
        # to be overridden
        pass

    def update_symbol(self):
        """
        Verändert das Aussehen eines Turms, abhängig von seine Power-Level
        :return:
        """
        path = self.get_symbol_path()

        new_symbol_path = re.sub("\d", str(self.attack_power_level), path)
        self.set_symbol_path(new_symbol_path)

    def get_upgrade_speed_cost(self):
        """
        Gibt die Kosten für Geschwindigkeits-Upgrades zurück.
        :return: int
        """
        return self.speed_upgrade_cost

    def draw_range(self, win):
        """
        Zeichnet einen Kreis um den Turm, mit dem Radius seiner Reichweite.
        :param win:
        :return:
        """
        pygame.draw.circle(win, [0, 200, 200, 50], self.get_center(), self.range, 2)

    def get_range_level(self):
        return self.range_level

    def get_speed_level(self):
        """
        Liefert das Attack-Speed Level zurück.
        :return: int
        """
        return self.speed_level

    def get_power_level(self):
        """
        Liefert das Power Level zurück.
        :return: int
        """
        return self.attack_power_level

    def fibonacci(self, num):
        """
        Errechnet eine Fibonacci-Folge.
        :param num:
        :return:
        """
        arr = [0, 1]
        if num == 1:
            return 1
        elif num == 2:
            return 2
        else:
            while (len(arr) < num):
                arr.append(0)
            if (num == 0 or num == 1):
                return 1
            else:
                arr[0] = 0
                arr[1] = 1
                for i in range(2, num):
                    arr[i] = arr[i - 1] + arr[i - 2]

        return arr.pop()
