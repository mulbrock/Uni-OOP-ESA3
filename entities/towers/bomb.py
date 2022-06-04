import pygame
import time
import math
from entities.towers.tower import Tower
from entities.towers.projectile import Projectile


class BombTower(Tower):

    cost = 10

    def __init__(self, _pos: tuple):
        _symbol_path = "assets/img/towers/bomb_1.png"
        _range = 150
        _cool_down = 3.0
        _attack_power = 1

        _cost = BombTower.cost
        super().__init__(_pos, _symbol_path, _range, _cool_down, _attack_power, _cost)

        self.projectiles = list()
        self.position_to_attack = (0, 0)

    def attack(self):
        if self.active:
            if time.time() - self.timer >= self.cool_down_time:
                self.timer = time.time()
                self.position_to_attack = self.aimed_enemy.get_center()

                projectile = Projectile(self.center, self.position_to_attack, self.attack_power, self.attack_power_level)
                self.projectiles.append(projectile)
                return True
        return False

    def draw_attack(self, win):
        for projectile in self.projectiles:
            projectile.draw_projectile(win)

    def get_impacted_projectiles(self):
        impacted_projectiles = list()
        for projectile in self.projectiles:
            if projectile.is_impacted():
                impacted_projectiles.append(projectile)
        for impacted in impacted_projectiles:
            self.projectiles.remove(impacted)
        return impacted_projectiles

    def upgrade_speed(self):
        if self.speed_level < 10:
            self.speed_upgrade_cost += self.speed_level
            self.cool_down_time -= 0.15
            self.speed_level += 1
            return True
        return False

    def increase_cost(self):
        BombTower.cost += 1

    def decrease_cost(self):
        BombTower.cost -= 1

    def redeem_coins(self):
        return BombTower.cost - 1