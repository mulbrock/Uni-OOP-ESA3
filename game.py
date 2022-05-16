import math
import time
import pygame
from pygame.locals import *

from utils.map import Map
from entities.enemies.enemy_one import EnemyOne
from entities.enemies.enemy_two import EnemyTwo
from entities.enemies.enemy_three import EnemyThree
from entities.towers.laser import LaserTower
from entities.towers.bomb import BombTower
from menus.ingame_menu import IngameMenu


class Game:

    def __init__(self, win, main_menu):
        self.win = win
        self.game_map = Map("01")

        self.building_mode = False
        self.active_building_area = None
        self.tower_to_build = None
        self.selected_tower = None

        self.impacted_projectiles = list()

        self.timer = time.time()
        self.spawn_cool_down = 0.5
        self.generate_enemies_cool_down = 2.0

        self.enemies_to_enter = list()
        self.wave = 1

        self.main_menu = main_menu

        # Ingame Menu positioning
        self.ingame_menu = IngameMenu()
        menu_pos = self.win.get_width()/2 - self.ingame_menu.get_width()/2, \
                   self.win.get_height() - self.ingame_menu.get_height()
        self.ingame_menu.set_draw_pos(menu_pos)

        # Stats
        self.money = 20
        self.lives = 20

        self.keep_going = True
        self.pause = False

    def start(self):

        # Display config

        # Entities
        bg = self.game_map.get_bg()
        self.generate_enemies()
        self.enemies_to_enter.reverse()
        building_areas = self.game_map.get_building_areas()

        # Action --> ALTER
        # Assign variables
        clock = pygame.time.Clock()

        # Loop
        while self.keep_going:

            if self.pause:
                self.main_menu.show_menu()
            else:
                # Timer
                clock.tick(90)
                self.win.blit(bg, (0, 0))

                # Enemies: Spawn and Creation
                if time.time() - self.timer >= self.spawn_cool_down and len(self.enemies_to_enter) > 0:
                    self.spawn_enemies()
                    self.timer = time.time()
                elif time.time() - self.timer >= self.generate_enemies_cool_down:
                    self.timer = time.time()
                    self.generate_enemies()
                    self.enemies_to_enter.reverse()

                # Event handling
                m_pos = pygame.mouse.get_pos()
                self.active_building_area = None
                for area in building_areas:
                    self.win.blit(area.get_image(), area.get_a())
                    if area.hover_check(m_pos):
                        self.active_building_area = area

                # Mouse clicks
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.keep_going = False
                        self.main_menu.end_game()
                        exit(0)
                    if event.type == MOUSEBUTTONDOWN:
                        left, middle, right = pygame.mouse.get_pressed()

                        # DELETE TOWER
                        if middle:
                            for t in self.game_map.get_all_towers():
                                if t.click_check(m_pos):
                                    self.remove_tower(t)
                                    if self.selected_tower == t:
                                        self.selected_tower = None
                                    break

                        # Building Mode stuff
                        if right and self.building_mode:
                            self.tower_to_build = BombTower(m_pos)

                        elif right and not self.building_mode:
                            self.building_mode = True
                            self.tower_to_build = LaserTower(m_pos)

                        elif left and self.building_mode:
                            if self.active_building_area is not None:

                                if self.active_building_area.is_tower_in_building_area(self.tower_to_build):
                                    if self.active_building_area.is_building_space_empty(self.tower_to_build):
                                        self.active_building_area.add_building(self.tower_to_build)
                                        self.building_mode = False

                        # Click detection, if mouse-position is on tower
                        elif left and not self.building_mode:
                            if self.ingame_menu.click_check(m_pos):
                                self.pause = True
                            else:
                                for tower in self.game_map.get_all_towers():
                                    if tower.click_check(m_pos):
                                        self.selected_tower = tower
                                        break
                                if self.selected_tower is not None:
                                    if not self.selected_tower.click_check(m_pos):
                                        self.selected_tower = None

                self.draw_ingame_menu()
                self.show_selected_tower()
                self.handle_tower_attack()
                self.handle_bomb_impacts()
                self.draw_entities(self.win)

            # Redisplay
            pygame.display.update()

    def draw_entities(self, win):
        self.draw_enemies(win)
        self.draw_towers(win)
        self.draw_tower_to_build(win)

    def handle_tower_attack(self):
        for tower in self.game_map.get_all_towers():
            tower.set_aimed_enemy(self.game_map.get_enemies())
            if tower.__class__ == BombTower:
                tower.attack()
                tower.draw_attack(self.win)
                self.impacted_projectiles.extend(tower.get_impacted_projectiles())
            elif tower.attack():
                tower.draw_attack(self.win)

    def handle_bomb_impacts(self):
        for projectile in self.impacted_projectiles:
            projectile.handle_impact(self.game_map.get_enemies())
        self.impacted_projectiles = list()

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

    def show_selected_tower(self):
        if self.selected_tower is not None:
            self.selected_tower.draw_range(self.win)

    def remove_tower(self, tower):
        self.game_map.remove_tower(tower)

    def draw_ingame_menu(self):
        self.win.blit(self.ingame_menu.get_symbol(), self.ingame_menu.get_draw_pos())

    def resume_game(self):
        self.pause = False

    def end_game(self):
        self.pause = False
        self.keep_going = False
