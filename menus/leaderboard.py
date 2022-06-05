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
        self.entries = []
        self.get_data()

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

        background = pygame.image.load("assets/img/leaderboard/leaderboard.png").\
            convert_alpha()
        draw_pos = (0, 0)
        super().__init__(draw_pos, background)

    def get_lowest(self):
        if len(self.entries) < 10:
            return 0
        else:
            return self.entries[9]["kills"]

    def get_data(self):
        self.entries.clear()
        with open("assets/leaderboard_data.json", "r") as json_file:
            data = json.load(json_file)
            for entry in data["entries"]:
                self.entries.append(entry)

    def draw_scores(self):
        y = 102
        for i in range(0, len(self.entries)):
            self.win.blit(self.entry_images[i], (50, y))

            name_font = pygame.font.Font("assets/orbitron-black.otf", 24)
            name_font = name_font.render(self.entries[i]["name"], True, (255, 255, 255))
            self.win.blit(name_font, (174, y+15))

            kills_font = pygame.font.Font("assets/orbitron-black.otf", 24)
            kills_font = kills_font.render(str(self.entries[i]["kills"]), True,
                                           (255, 255, 255))
            self.win.blit(kills_font, (625, y+15))

            y += 65

    def update_leaderboard(self, name, new_score):
        self.entries.append({"name": name, "kills": new_score})

        self.entries = sorted(self.entries, key=lambda d: d["kills"], reverse=True)

        if len(self.entries) == 11:
            del self.entries[10]

        updated_entries = {
            "entries":
                self.entries
        }

        json_string = json.dumps(updated_entries)
        with open("assets/leaderboard_data.json", "w") as json_file:
            json_file.write(json_string)

        self.get_data()

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