import math

import pygame
from pygame.locals import *

from utils.map import Map
from entities.enemies.enemy_one import EnemyOne
from entities.towers.laser import LaserTower


class Game:

    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption("Tower Defense")
        self.game_map = Map("01")
        self.building_mode = False
        self.tower_to_build = None

    def start(self):

        # Display config

        # Entities
        bg = self.game_map.get_bg()
        en = EnemyOne(self.game_map.get_path())
        self.game_map.add_enemy(en)

        # Action --> ALTER
        # Assign variables
        keep_going = True
        clock = pygame.time.Clock()

        # Loop
        while keep_going:

            # Timer
            clock.tick(90)
            self.win.blit(bg, (0, 0))

            # Event handling
            m_pos = pygame.mouse.get_pos()
            area = self.game_map.hover_check(m_pos)
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

                    if right:
                        self.building_mode = True
                        self.tower_to_build = LaserTower(m_pos)
                    elif left and self.building_mode:
                        for area in self.game_map.get_building_areas():
                            print(area.is_tower_in_building_area(self.tower_to_build))
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
            win.blit(enemy.get_symbol(), enemy.get_draw_pos())
            enemy.draw_life(win)
            if not enemy.move_forward():
                self.game_map.remove_enemy(enemy)

    def draw_towers(self, win):
        for tower in self.game_map.get_all_towers():
            win.blit(tower.get_symbol(), tower.get_draw_pos())

    def draw_tower_to_build(self, win):
        if self.tower_to_build is not None and self.building_mode:

            win.blit(self.tower_to_build.get_symbol(), self.tower_to_build.get_draw_pos())

