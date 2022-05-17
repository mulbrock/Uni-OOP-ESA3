import pygame
from pygame.locals import *

from game import Game
from menus.menu import Menu
from menus.save_menu import SaveMenu
from menus.buttons.button import Button


class MainMenu(Menu):

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tower Defense")

        self.win = pygame.display.set_mode((1024, 768))
        background = pygame.image.load("assets/img/menu/main_menu.png").convert_alpha()

        draw_pos = (0, 0)

        super().__init__(draw_pos, background)

        self.current_game = None
        self.init_buttons()
        self.menu_shown = True

        self.save_menu = SaveMenu(self.win)

    def init_buttons(self):
        new_game_button = Button("mbtn_new_game")
        new_game_button.set_draw_pos((50, 220))
        new_game_button.click = lambda: self.new_game_button_clicked()
        self.add_button(new_game_button)

        resume_game_button = Button("mbtn_continue")
        resume_game_button.set_draw_pos((537, 220))
        resume_game_button.click = lambda: self.resume_game_button_clicked()
        self.add_button(resume_game_button)

        tutorial_button = Button("mbtn_tutorial")
        tutorial_button.set_draw_pos((50, 390))
        tutorial_button.click = lambda: self.tutorial_button_clicked()
        self.add_button(tutorial_button)

        scoreboard_button = Button("mbtn_ranking")
        scoreboard_button.set_draw_pos((537, 390))
        scoreboard_button.click = lambda: self.scoreboard_button_clicked()
        self.add_button(scoreboard_button)

        end_button = Button("mbtn_quit")
        end_button.set_draw_pos((537, 560))
        end_button.click = lambda: self.end_game()
        self.add_button(end_button)

    def get_window(self):
        return self.win

    def show_menu(self):
        self.menu_shown = True
        while self.menu_shown:
            self.win.blit(self.background, self.draw_pos)

            m_pos = pygame.mouse.get_pos()
            for button in self.buttons.values():
                self.win.blit(button.get_symbol(), button.get_draw_pos())

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.menu_shown = False
                    if self.current_game is not None:
                        self.current_game.end_game()
                    exit(0)
                if event.type == MOUSEBUTTONDOWN:
                    left, middle, right = pygame.mouse.get_pressed()
                    if left:
                        for button in self.buttons.values():
                            if button.click_check(m_pos):
                                button.click()

            # Redisplay
            pygame.display.update()

    def new_game_button_clicked(self):

        self.current_game = None
        self.current_game = Game(self.win, self)
        self.menu_shown = False
        self.current_game.start()

    def resume_game_button_clicked(self):
        if self.current_game is None:
            print("No game running")
        else:
            self.current_game.resume_game()
            self.menu_shown = False

    def tutorial_button_clicked(self):
        print('tutorial')

    def scoreboard_button_clicked(self):
        print('scoreboard')

    def save_game_clicked(self):
        if self.current_game is None:
            print("No game running")
        else:
            self.save_menu.draw()
            print("save")

    def end_game(self):
        self.menu_shown = False
        exit(0)