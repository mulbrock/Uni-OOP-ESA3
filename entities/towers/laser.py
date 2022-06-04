import pygame
import time
from entities.towers.tower import Tower

class LaserTower(Tower):

    cost = 4

    def __init__(self, pos: tuple):
        _symbol_path = "assets/img/towers/laser_1.png"
        _range = 100
        _cool_down = 0.5
        _attack_power = 0.5

        _cost = LaserTower.cost
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
            enemy_pos = self.aimed_enemy.get_center()
            beam_origin_pos = self.get_center()

            if self.attack_power_level == 1:
                pygame.draw.line(win, (0, 255, 0), beam_origin_pos, enemy_pos, 1)
            elif self.attack_power_level == 2:
                pygame.draw.line(win, (0, 255, 0), beam_origin_pos, enemy_pos, 3)
            elif self.attack_power_level == 3:
                pygame.draw.line(win, (0, 255, 0), beam_origin_pos, enemy_pos, 6)
            elif self.attack_power_level == 4:
                pygame.draw.line(win, (0, 0, 255), beam_origin_pos, enemy_pos, 2)
            elif self.attack_power_level == 5:
                pygame.draw.line(win, (0, 0, 255), beam_origin_pos, enemy_pos, 5)
            elif self.attack_power_level == 6:
                pygame.draw.line(win, (0, 0, 255), beam_origin_pos, enemy_pos, 8)
            elif self.attack_power_level == 7:
                pygame.draw.line(win, (255, 0, 0), beam_origin_pos, enemy_pos, 4)
            elif self.attack_power_level == 8:
                pygame.draw.line(win, (255, 0, 0), beam_origin_pos, enemy_pos, 7)
            elif self.attack_power_level == 9:
                pygame.draw.line(win, (255, 0, 0), beam_origin_pos, enemy_pos, 10)
            else:
                pygame.draw.line(win, (255, 0, 0), beam_origin_pos, enemy_pos, 13)

    def upgrade_speed(self):
        if self.speed_level < 10:
            self.speed_upgrade_cost += self.speed_level
            self.cool_down_time -= 0.02
            self.speed_level += 1
            return True
        return False

    def increase_cost(self):
        LaserTower.cost += 1

    def decrease_cost(self):
        LaserTower.cost -= 1

    def redeem_coins(self):
        return LaserTower.cost - 1