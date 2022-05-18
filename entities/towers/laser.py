import pygame
import time
from entities.towers.tower import Tower


class LaserTower(Tower):

    COST = 4

    def __init__(self, pos: tuple):
        _symbol_path = "assets/img/towers/laser_1.png"
        _range = 100
        _cool_down = 0.5
        _attack_power = 0.5

        _cost = LaserTower.COST
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

            beam_num = int(self.attack_power_level / 3) + 1

            for beam in range(1, beam_num + 1):
                print(beam)
                if beam == 1:

                    pygame.draw.line(win, (0, 255, 255), beam_origin_pos, enemy_pos, (2))
                if beam == 2:

                    enemy_pos = enemy_pos[0] - 10, enemy_pos[1] - 10
                    pygame.draw.line(win, (0, 0, 255), beam_origin_pos, enemy_pos, (2))

