import math
import time
import pygame
from pygame.locals import *

from utils.map import Map
from entities.enemies.enemy_one import EnemyOne
from entities.enemies.enemy_two import EnemyTwo
from entities.enemies.enemy_three import EnemyThree
from entities.towers.laser import LaserTower


class Game:

    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption("Tower Defense")
        self.game_map = Map("01")
        self.building_mode = False
        self.tower_to_build = None

        self.timer = time.time()
        self.spawn_cool_down = 2.0
        self.cast_cool_down = 2.0

        self.enemies_to_enter = list()
        self.wave = 1

        #stats
        self.money = 20
        self.lives = 20

    def start(self):

        # Display config

        # Entities
        bg = self.game_map.get_bg()
        self.generate_enemies()
        self.enemies_to_enter.reverse()

        # Action --> ALTER
        # Assign variables
        keep_going = True
        clock = pygame.time.Clock()

        # Loop
        while keep_going:

            # Timer
            clock.tick(200)
            self.win.blit(bg, (0, 0))

            # Event handling
            m_pos = pygame.mouse.get_pos()
            area = self.game_map.hover_check(m_pos)

            if time.time() - self.timer >= self.spawn_cool_down and len(self.enemies_to_enter) > 0:
                self.spawn_enemies()
                self.timer = time.time()
            elif time.time() - self.timer >= self.cast_cool_down:
                self.timer = time.time()
                self.generate_enemies()
                self.enemies_to_enter.reverse()

            if area is not None:
                self.win.blit(area.get_image(), area.get_a())

            if self.building_mode:
                self.tower_to_build = LaserTower(m_pos)

            for event in pygame.event.get():
                if event.type == QUIT:
                    keep_going = False
                    break
                if event.type == MOUSEBUTTONDOWN:
                    left, middle, right = pygame.mouse.get_pressed()

                    if right and self.building_mode == True:
                        self.tower_to_build = LaserTower(m_pos)
                    elif right and not self.building_mode:
                        self.building_mode = True
                        self.tower_to_build = LaserTower(m_pos)
                    elif left and self.building_mode:
                        for area in self.game_map.get_building_areas():
                            if area.is_tower_in_building_area(self.tower_to_build):
                                if area.is_building_space_empty(self.tower_to_build):
                                    area.add_building(self.tower_to_build)
                                    self.building_mode = False

            self.handle_tower_attack()

            self.draw_entities(self.win)
            # Redisplay
            pygame.display.update()

    def handle_tower_attack(self):
        for tower in self.game_map.get_all_towers():
            tower.set_aimed_enemy(self.game_map.get_enemies())
            if tower.attack():
                tower.draw_attack(self.win)

    def draw_entities(self, win):
        self.draw_enemies(win)
        self.draw_towers(win)
        self.draw_tower_to_build(win)

    def draw_enemies(self, win):
        for enemy in self.game_map.get_enemies():
            if enemy.get_life() <= 0:
                self.game_map.remove_enemy(enemy)
                self.money += enemy.kill_reward
            win.blit(enemy.get_symbol(), enemy.get_draw_pos())
            enemy.draw_life(win)
            if not enemy.move_forward():
                self.game_map.remove_enemy(enemy)
                self.lives -= 1

    def draw_towers(self, win):
        for tower in self.game_map.get_all_towers():
            win.blit(tower.get_symbol(), tower.get_draw_pos())

    def draw_tower_to_build(self, win):
        if self.tower_to_build is not None and self.building_mode:

            win.blit(self.tower_to_build.get_symbol(), self.tower_to_build.get_draw_pos())

    def spawn_enemies(self):
        if len(self.enemies_to_enter) > 0:
            enemy = self.enemies_to_enter.pop()
            if enemy:
                self.game_map.add_enemy(enemy)
        else:
            self.wave += 1

    def generate_enemies(self):
        amount = 20
        amount *= self.wave
        for i in range(1, amount):
            if i % 4 == 0:
                enemy = EnemyTwo(self.game_map.get_path())
                enemy.increase_max_hp_by(self.wave * 3)
            elif i % (amount-1) == 0:
                enemy = EnemyThree(self.game_map.get_path())
                enemy.increase_max_hp_by(self.wave * 6)
            else:
                enemy = EnemyOne(self.game_map.get_path())
                enemy.increase_max_hp_by(self.wave * 2)
            self.enemies_to_enter.append(enemy)
