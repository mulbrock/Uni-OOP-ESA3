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
        self.destroy_mode = False
        self.building_laser = False
        self.building_bomb = False
        self.active_building_area = None
        self.tower_to_build = None
        self.selected_tower = None
        self.ingame_menu_button_pressed = False
        self.unbuilt_tower = None       # wird am Cursor befestigt, wenn gebaut werden soll

        self.left_menu_button_down = False
        self.middle_menu_button_down = False
        self.right_menu_button_down = False
        self.pause_button_down = False

        self.impacted_projectiles = list()

        self.timer = time.time()
        self.spawn_cool_down = 0.5
        self.generate_enemies_cool_down = 5.0
        self.all_enemies_killed = True

        self.enemies_to_enter = list()

        self.main_menu = main_menu

        # Ingame Menu positioning
        self.ingame_menu = IngameMenu()

        # Stats
        self.money = 20
        self.lives = 20
        self.wave = 1
        self.kills = 0
        self.enemies = 0

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
                elif time.time() - self.timer >= self.generate_enemies_cool_down and self.all_enemies_killed:
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
                    elif event.type == MOUSEBUTTONDOWN:
                        left, middle, right = pygame.mouse.get_pressed()

                        # Destroy Tower
                        if left and self.destroy_mode:
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
                            if self.ingame_menu.left_btn_check(m_pos):
                                self.left_menu_button_down = True
                                self.ingame_menu.get_buttons()[0].button_down()
                            elif self.ingame_menu.middle_btn_check(m_pos):
                                self.middle_menu_button_down = True
                                self.ingame_menu.get_buttons()[1].button_down()
                            elif self.ingame_menu.right_btn_check(m_pos):
                                self.right_menu_button_down = True
                                self.ingame_menu.get_buttons()[2].button_down()
                            elif self.ingame_menu.pause_check(m_pos):
                                self.pause_button_down = True
                                self.ingame_menu.get_buttons()[3].button_down()
                            else:
                                for tower in self.game_map.get_all_towers():
                                    if tower.click_check(m_pos):
                                        self.selected_tower = tower
                                        break
                                if self.selected_tower is not None:
                                    if not self.selected_tower.click_check(m_pos):
                                        self.selected_tower = None

                    elif event.type == MOUSEBUTTONUP:
                        for button in self.ingame_menu.get_buttons():
                            button.button_up()
                        if self.ingame_menu.pause_check(m_pos) and self.pause_button_down:
                            self.pause = True
                        elif self.ingame_menu.left_btn_check(m_pos) and self.left_menu_button_down:
                            if self.ingame_menu.upgrade_mode:
                                print('upgrade range')
                            else:
                                print('build laser')
                                self.building_bomb = False
                                self.destroy_mode = False
                                self.building_laser = True
                        elif self.ingame_menu.middle_btn_check(m_pos) and self.middle_menu_button_down:
                            if self.ingame_menu.upgrade_mode:
                                print('upgrade frequency')
                            else:
                                print('build bomb')
                                self.building_laser = False
                                self.destroy_mode = False
                                self.building_bomb = True
                        elif self.ingame_menu.right_btn_check(m_pos) and self.right_menu_button_down:
                            if self.ingame_menu.upgrade_mode:
                                print('upgrade power')
                            else:
                                print('destroy mode')
                                self.building_laser = False
                                self.building_bomb = False
                                self.destroy_mode = True
                        else:
                            self.destroy_mode = False

                        self.left_menu_button_down = False
                        self.middle_menu_button_down = False
                        self.right_menu_button_down = False
                        self.pause_button_down = False

                self.draw_ingame_menu()
                self.show_selected_tower()
                self.handle_tower_attack()
                self.handle_bomb_impacts()
                self.draw_entities(self.win)
                self.print_stats()
                self.update_stats()

            if len(self.game_map.get_enemies()) == 0:
                self.all_enemies_killed = True
            else:
                self.all_enemies_killed = False
            # Redisplay
            pygame.display.update()

    def draw_entities(self, win):
        self.draw_enemies(win)
        self.draw_towers(win)
        self.draw_tower_to_build(win)

    def update_stats(self):
        self.enemies = len(self.game_map.get_enemies())

    def print_stats(self):
        lives_font = pygame.font.Font("freesansbold.ttf", 24)
        lives_font = lives_font.render(str(self.lives), True, (255, 255, 255))
        self.win.blit(lives_font, (75, 726))

        coin_font = pygame.font.Font("freesansbold.ttf", 24)
        coin_font = coin_font.render(str(self.money), True, (255, 255, 255))
        self.win.blit(coin_font, (250, 726))

        kill_font = pygame.font.Font("freesansbold.ttf", 24)
        kill_font = kill_font.render(str(self.kills), True, (255, 255, 255))
        self.win.blit(kill_font, (425, 726))

        enemy_font = pygame.font.Font("freesansbold.ttf", 24)
        enemy_font = enemy_font.render(str(self.enemies), True, (255, 255, 255))
        self.win.blit(enemy_font, (600, 726))

        wave_font = pygame.font.Font("freesansbold.ttf", 24)
        wave_font = wave_font.render(str(self.wave), True, (255, 255, 255))
        self.win.blit(wave_font, (775, 726))

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
        for button in self.ingame_menu.get_buttons():
            self.win.blit(button.get_symbol(), button.get_draw_pos())

    def resume_game(self):
        self.pause = False

    def end_game(self):
        self.pause = False
        self.keep_going = False
