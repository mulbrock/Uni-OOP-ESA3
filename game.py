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
        self.destroy_symbol = pygame.image.load("assets/img/delete.png").convert_alpha()

        # Modes
        self.menu_in_building_mode = True
        self.destroy_mode = False
        self.building_laser = False
        self.building_bomb = False

        # Active Entities / Areas
        self.active_building_area = None
        self.tower_to_build = None
        self.selected_tower = None

        # Ingame Menu Buttons
        self.ingame_menu_button_pressed = False
        self.left_menu_button_down = False
        self.middle_menu_button_down = False
        self.right_menu_button_down = False
        self.pause_button_down = False
        self.button_up_after_build = False

        # Projectiles
        self.impacted_projectiles = list()

        # Enemies
        self.timer = time.time()
        self.spawn_cool_down = 0.5
        self.generate_enemies_cool_down = 5.0
        self.all_enemies_killed = True
        self.enemies_to_enter = list()
        self.amount = 9

        # Main Menu
        self.main_menu = main_menu

        # Ingame Menu
        self.ingame_menu = IngameMenu()

        # Game Over
        self.game_over = False
        self.game_over_overlay = pygame.image.load("assets/img/game_over.png").convert_alpha()

        # Stats
        self.money = 20
        self.lives = 20
        self.wave = 1
        self.kills = 0
        self.enemies = 0

        # Run Game
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
        while self.keep_going and not self.game_over:

            if self.pause:
                self.main_menu.show_menu()
            else:
                # Timer
                clock.tick(60)
                self.win.blit(bg, (0, 0))

                # Game Over
                if self.lives == 0:
                    self.game_over = True

                # Enemies: Spawn and Creation
                if time.time() - self.timer >= self.spawn_cool_down and len(self.enemies_to_enter) > 0:
                    self.spawn_enemies()
                    self.timer = time.time()
                elif time.time() - self.timer >= self.generate_enemies_cool_down and self.all_enemies_killed:
                    self.wave += 1
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
                self.button_up_after_build = False

                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.keep_going = False
                        self.main_menu.end_game()

                    elif event.type == MOUSEBUTTONDOWN:
                        left, middle, right = pygame.mouse.get_pressed()

                        # Unselect Tower to Build / Destroy
                        if right and (self.building_bomb or self.building_laser or self.destroy_mode):
                            self.tower_to_build = None
                            self.building_laser = False
                            self.building_bomb = False
                            self.destroy_mode = False

                        # Destroy Tower
                        if left and self.destroy_mode:
                            for t in self.game_map.get_all_towers():
                                if t.click_check(m_pos):
                                    self.remove_tower(t)
                                    if self.selected_tower == t:
                                        self.selected_tower = None
                                    break

                        # Build Tower
                        if left and (self.building_bomb or self.building_laser):
                            if self.active_building_area is not None:
                                self.tower_to_build.set_center(m_pos)
                                if self.active_building_area.is_tower_in_building_area(self.tower_to_build):
                                    if self.active_building_area.is_building_space_empty(self.tower_to_build):
                                        self.money -= self.tower_to_build.COST
                                        self.active_building_area.add_building(self.tower_to_build, m_pos)
                                        self.building_bomb = False
                                        self.building_laser = False
                                        self.button_up_after_build = True

                        # Click detection, if mouse-position is on tower
                        if left:
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
                            elif not (self.building_bomb or self.building_laser) and not self.button_up_after_build:
                                for tower in self.game_map.get_all_towers():
                                    if tower.click_check(m_pos):
                                        self.selected_tower = tower
                                        self.menu_in_building_mode = False
                                        self.ingame_menu.switch_to_upgrade_view()
                                        break
                                if self.selected_tower is not None:
                                    if not self.selected_tower.click_check(m_pos):
                                        self.selected_tower = None
                                        self.ingame_menu.switch_to_build_view()
                                        self.menu_in_building_mode = True

                    # Upgrading / Activating Build
                    elif event.type == MOUSEBUTTONUP:
                        for button in self.ingame_menu.get_buttons():
                            button.button_up()
                        if self.ingame_menu.pause_check(m_pos) and self.pause_button_down:
                            self.pause = True
                        elif self.ingame_menu.left_btn_check(m_pos) and self.left_menu_button_down:
                            if self.ingame_menu.upgrade_mode:
                                if self.selected_tower is not None:
                                    update_cost = self.selected_tower.get_upgrade_range_cost()
                                    if self.money >= update_cost:
                                        if self.selected_tower.upgrade_range():
                                            self.money -= update_cost
                            else:
                                if self.money >= LaserTower.COST:
                                    self.building_bomb = False
                                    self.destroy_mode = False
                                    self.building_laser = True
                                    self.tower_to_build = LaserTower(m_pos)
                        elif self.ingame_menu.middle_btn_check(m_pos) and self.middle_menu_button_down:
                            if self.ingame_menu.upgrade_mode:
                                if self.selected_tower is not None:
                                    update_cost = self.selected_tower.get_upgrade_speed_cost()
                                    if self.money >= update_cost:
                                        if self.selected_tower.upgrade_speed():
                                            self.money -= update_cost
                            else:
                                if self.money >= BombTower.COST:
                                    self.building_laser = False
                                    self.destroy_mode = False
                                    self.building_bomb = True
                                    self.tower_to_build = BombTower(m_pos)
                        elif self.ingame_menu.right_btn_check(m_pos) and self.right_menu_button_down:
                            if self.ingame_menu.upgrade_mode:
                                if self.selected_tower is not None:
                                    update_cost = self.selected_tower.get_upgrade_power_cost()
                                    if self.money >= update_cost:
                                        if self.selected_tower.upgrade_power():
                                            print('upgrade power')
                                            self.money -= update_cost
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

                if self.destroy_mode:
                    self.draw_destroy_symbol(self.win, m_pos)

                if self.building_laser or self.building_bomb:
                    self.draw_tower_to_build(self.win, m_pos)

                if self.menu_in_building_mode:
                    self.print_building_cost()
                else:
                    self.print_tower_levels()
                    self.print_upgrade_cost()

            if len(self.game_map.get_enemies()) == 0:
                self.all_enemies_killed = True
            else:
                self.all_enemies_killed = False

            # Redisplay
            pygame.display.update()

        while self.keep_going and self.game_over:
            self.win.blit(bg, (0, 0))
            self.win.blit(self.game_over_overlay, (0, 0))

            self.main_menu.game_over()

            m_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.keep_going = False
                    self.main_menu.end_game()

                elif event.type == MOUSEBUTTONUP:
                    self.keep_going = False
                    self.main_menu.show_menu()

            pygame.display.update()

    # Drawing
    def draw_entities(self, win):
        self.draw_enemies(win)
        self.draw_towers(win)

    def draw_enemies(self, win):
        for enemy in self.game_map.get_enemies():
            if enemy.get_life() <= 0:
                self.game_map.remove_enemy(enemy)
                self.money += enemy.kill_reward
                self.kills += 1
            win.blit(enemy.get_symbol(), enemy.get_draw_pos())
            enemy.draw_life(win)
            if not enemy.move_forward():
                self.game_map.remove_enemy(enemy)
                self.lives -= 1

    def draw_tower_to_build(self, win, m_pos):
        x, y = m_pos
        if type(self.tower_to_build) == LaserTower:
            x -= 10
            y -= 10
        else:
            x -= 22
            y -= 22
        win.blit(self.tower_to_build.get_symbol(), (x, y))

    def draw_destroy_symbol(self, win, m_pos):
        x, y = m_pos
        x -= 12
        y -= 12
        win.blit(self.destroy_symbol, (x, y))

    def draw_towers(self, win):
        for tower in self.game_map.get_all_towers():
            win.blit(tower.get_symbol(), tower.get_draw_pos())

    def show_selected_tower(self):
        if self.selected_tower is not None:
            self.selected_tower.draw_range(self.win)

    def draw_ingame_menu(self):
        self.win.blit(self.ingame_menu.get_symbol(), self.ingame_menu.get_draw_pos())
        for button in self.ingame_menu.get_buttons():
            self.win.blit(button.get_symbol(), button.get_draw_pos())

    # Printing Stats and Costs
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

    def print_building_cost(self):
        if self.money >= BombTower.COST:
            laser_print_color = (255, 255, 255)
            bomb_print_color = (255, 255, 255)
        elif self.money >= LaserTower.COST:
            laser_print_color = (255, 255, 255)
            bomb_print_color = (255, 0, 0)
        else:
            laser_print_color = (255, 0, 0)
            bomb_print_color = (255, 0, 0)

        laser_cost_font = pygame.font.Font("freesansbold.ttf", 24)
        laser_cost_font = laser_cost_font.render(str(LaserTower.COST), True, laser_print_color)
        self.win.blit(laser_cost_font, (277, 668))

        bomb_cost_font = pygame.font.Font("freesansbold.ttf", 24)
        bomb_cost_font = bomb_cost_font.render(str(BombTower.COST), True, bomb_print_color)
        self.win.blit(bomb_cost_font, (566, 668))

    def print_upgrade_cost(self):
        if self.selected_tower.get_speed_level() < 10:
            if self.money >= self.selected_tower.get_upgrade_speed_cost():
                speed_print_color = (255, 255, 255)
            else:
                speed_print_color = (255, 0, 0)

            speed_cost_font = pygame.font.Font("freesansbold.ttf", 24)
            speed_cost_font = speed_cost_font.render(str(self.selected_tower.get_upgrade_speed_cost()), True, speed_print_color)
            self.win.blit(speed_cost_font, (566, 668))

        if self.selected_tower.get_range_level() < 10:
            if self.money >= self.selected_tower.get_upgrade_range_cost():
                range_print_color = (255, 255, 255)
            else:
                range_print_color = (255, 0, 0)

            range_cost_font = pygame.font.Font("freesansbold.ttf", 24)
            range_cost_font = range_cost_font.render(str(self.selected_tower.get_upgrade_range_cost()), True, range_print_color)
            self.win.blit(range_cost_font, (270, 668))

        if self.selected_tower.get_power_level() < 10:
            if self.money >= self.selected_tower.get_upgrade_power_cost():
                power_print_color = (255, 255, 255)
            else:
                power_print_color = (255, 0, 0)

            power_cost_font = pygame.font.Font("freesansbold.ttf", 24)
            power_cost_font = power_cost_font.render(str(self.selected_tower.get_upgrade_power_cost()), True, power_print_color)
            self.win.blit(power_cost_font, (861, 668))

    def print_tower_levels(self):
        range_level_font = pygame.font.Font("freesansbold.ttf", 24)
        range_level_font = range_level_font.render(str(self.selected_tower.get_range_level()), True, (255, 255, 255))
        self.win.blit(range_level_font, (270, 583))

        speed_level_font = pygame.font.Font("freesansbold.ttf", 24)
        speed_level_font = speed_level_font.render(str(self.selected_tower.get_speed_level()), True, (255, 255, 255))
        self.win.blit(speed_level_font, (566, 583))

        power_level_font = pygame.font.Font("freesansbold.ttf", 24)
        power_level_font = power_level_font.render(str(self.selected_tower.get_power_level()), True, (255, 255, 255))
        self.win.blit(power_level_font, (861, 583))

    # Updating
    def update_stats(self):
        self.enemies = len(self.game_map.get_enemies())

    # Handling
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

    # Creating Enemies
    def spawn_enemies(self):
        if len(self.enemies_to_enter) > 0:
            enemy = self.enemies_to_enter.pop()
            if enemy:
                self.game_map.add_enemy(enemy)

    def generate_enemies(self):
        if self.wave < 5:
            self.amount += self.wave
        else:
            self.amount += 5

        # 10 Enemies
        if self.wave == 1:
            for i in range(0, self.amount):
                enemy = EnemyOne(self.game_map.get_path())
                enemy.increase_max_hp_by(self.wave * 2)
                self.enemies_to_enter.append(enemy)

        # 12 Enemies
        elif self.wave == 2:
            for i in range(0, self.amount - 1):
                enemy = EnemyOne(self.game_map.get_path())
                enemy.increase_max_hp_by(self.wave * 2)
                self.enemies_to_enter.append(enemy)
            enemy = EnemyTwo(self.game_map.get_path())
            enemy.increase_max_hp_by(self.wave * 3)
            self.enemies_to_enter.append(enemy)

        # 15 Enemies
        elif self.wave == 3:
            for i in range(0, self.amount):
                if i > 0 and (i+1) % 5 == 0:
                    enemy = EnemyTwo(self.game_map.get_path())
                    enemy.increase_max_hp_by(self.wave * 3)
                    self.enemies_to_enter.append(enemy)
                else:
                    enemy = EnemyOne(self.game_map.get_path())
                    enemy.increase_max_hp_by(self.wave * 2)
                    self.enemies_to_enter.append(enemy)

        # 19 Enemies
        elif self.wave == 4:
            for i in range(0, self.amount):
                if i == self.amount-1:
                    enemy = EnemyThree(self.game_map.get_path())
                    enemy.increase_max_hp_by(self.wave * 6)
                elif i > 0 and (i+1) % 4 == 0:
                    enemy = EnemyTwo(self.game_map.get_path())
                    enemy.increase_max_hp_by(self.wave * 3)
                else:
                    enemy = EnemyOne(self.game_map.get_path())
                    enemy.increase_max_hp_by(self.wave * 2)
                self.enemies_to_enter.append(enemy)

        # 24 Enemies
        elif self.wave == 5:
            for i in range(0, self.amount):
                if i == self.amount - 1 or i == self.amount / 2:
                    enemy = EnemyThree(self.game_map.get_path())
                    enemy.increase_max_hp_by(self.wave * 6)
                elif i % 3 == 0:
                    enemy = EnemyTwo(self.game_map.get_path())
                    enemy.increase_max_hp_by(self.wave * 3)
                else:
                    enemy = EnemyOne(self.game_map.get_path())
                    enemy.increase_max_hp_by(self.wave * 2)
                self.enemies_to_enter.append(enemy)

        # 29 Enemies
        elif self.wave == 6:
            for i in range(0, self.amount):
                if i == self.amount - 1 or i == int(self.amount / 3) or i == int((self.amount * 2) / 3) or i == 0:
                    enemy = EnemyThree(self.game_map.get_path())
                    enemy.increase_max_hp_by(self.wave * 6)
                elif i % 2 == 0:
                    enemy = EnemyTwo(self.game_map.get_path())
                    enemy.increase_max_hp_by(self.wave * 3)
                else:
                    enemy = EnemyOne(self.game_map.get_path())
                    enemy.increase_max_hp_by(self.wave * 2)
                self.enemies_to_enter.append(enemy)

        # 34 Enemies
        elif self.wave == 7:
            for i in range(0, self.amount):
                if i > (self.amount * 2) / 3:
                    enemy = EnemyThree(self.game_map.get_path())
                    enemy.increase_max_hp_by(self.wave * 6)
                elif i > self.amount / 3:
                    enemy = EnemyTwo(self.game_map.get_path())
                    enemy.increase_max_hp_by(self.wave * 3)
                else:
                    enemy = EnemyOne(self.game_map.get_path())
                    enemy.increase_max_hp_by(self.wave * 2)
                self.enemies_to_enter.append(enemy)

        # 39 Enemies
        elif self.wave == 8:
            for i in range(0, self.amount):
                if i < 3 or i > self.amount - 4:
                    enemy = EnemyOne(self.game_map.get_path())
                    enemy.increase_max_hp_by(self.wave * 2)
                elif i < 8 or i > self.amount - 9 or i == 20:
                    enemy = EnemyTwo(self.game_map.get_path())
                    enemy.increase_max_hp_by(self.wave * 3)
                else:
                    enemy = EnemyThree(self.game_map.get_path())
                    enemy.increase_max_hp_by(self.wave * 6)
                self.enemies_to_enter.append(enemy)

        # 44 Enemies
        elif self.wave == 9:
            for i in range(0, self.amount):
                if i % 2 == 0 or i % 3 == 0:
                    enemy = EnemyThree(self.game_map.get_path())
                    enemy.increase_max_hp_by(self.wave * 6)
                else:
                    enemy = EnemyTwo(self.game_map.get_path())
                    enemy.increase_max_hp_by(self.wave * 3)
                self.enemies_to_enter.append(enemy)

        # 49 Enemies +
        else:
            for i in range(0, self.amount):
                enemy = EnemyThree(self.game_map.get_path())
                enemy.increase_max_hp_by(self.wave * 6)
                self.enemies_to_enter.append(enemy)

    # Removing
    def remove_tower(self, tower):
        self.game_map.remove_tower(tower)

    # General Functions
    def resume_game(self):
        self.pause = False

    def end_game(self):
        self.pause = False
        self.keep_going = False