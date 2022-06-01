import pygame
import json
from pygame.locals import *
from menus.menu import Menu
from menus.buttons.button import Button

class Leaderboard(Menu):

    def __init__(self, win, main_menu):
        self.win = win
        self.leaderboard_shown = False
        self.main_menu = main_menu
        self.score_list = []
        self.name_list = []

        self.back_button = Button('lbtn_back', draw_pos=(844, 687))
        self.entry_images = [
            pygame.image.load("assets/img/leaderboard/p1.png").convert_alpha(),
            pygame.image.load("assets/img/leaderboard/p2.png").convert_alpha(),
            pygame.image.load("assets/img/leaderboard/p3.png").convert_alpha(),
            pygame.image.load("assets/img/leaderboard/p4.png").convert_alpha(),
            pygame.image.load("assets/img/leaderboard/p5.png").convert_alpha(),
            pygame.image.load("assets/img/leaderboard/p6.png").convert_alpha(),
            pygame.image.load("assets/img/leaderboard/p7.png").convert_alpha(),
            pygame.image.load("assets/img/leaderboard/p8.png").convert_alpha(),
            pygame.image.load("assets/img/leaderboard/p9.png").convert_alpha(),
            pygame.image.load("assets/img/leaderboard/p10.png").convert_alpha()
        ]

        self.entries = self.get_data()
        background = pygame.image.load("assets/img/leaderboard/leaderboard.png").convert_alpha()
        draw_pos = (0, 0)
        super().__init__(draw_pos, background)

    def get_lowest(self):
        if len(self.score_list) < 10:
            return 0
        else:
            return self.score_list[9]

    def get_data(self):
        with open("assets/leaderboard_data.json", "r") as json_file:
            data = json.load(json_file)
            for entry in data["entries"]:
                self.score_list.append(entry["kills"])
                self.name_list.append(entry["name"])
            print(self.score_list)
        return data

    def draw_scores(self):
        y = 102
        for i in range(0, len(self.score_list)):
            self.win.blit(self.entry_images[i], (50, y))

            name_font = pygame.font.Font("assets/orbitron-black.otf", 24)
            name_font = name_font.render(self.name_list[i], True, (255, 255, 255))
            self.win.blit(name_font, (174, y+15))

            kills_font = pygame.font.Font("assets/orbitron-black.otf", 24)
            kills_font = kills_font.render(str(self.score_list[i]), True, (255, 255, 255))
            self.win.blit(kills_font, (625, y+15))

            y += 65

    def update_leaderboard(self, new_score):
        pass

    def show_leaderboard(self):
        self.leaderboard_shown = True
        while self.leaderboard_shown:
            self.win.blit(self.background, self.draw_pos)
            self.win.blit(self.back_button.get_symbol(), self.back_button.get_draw_pos())
            self.draw_scores()

            m_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit(0)

                if event.type == MOUSEBUTTONDOWN:
                    left, middle, right = pygame.mouse.get_pressed()
                    if left:
                        if self.back_button.click_check(m_pos):
                            self.back_button.button_down()
                if event.type == MOUSEBUTTONUP:
                    if self.back_button.click_check(m_pos) and self.back_button.pressed:
                        self.back_button.button_up()
                        self.leaderboard_shown = False
                        self.main_menu.show_menu()
                    else:
                        self.back_button.button_up()

            pygame.display.update()