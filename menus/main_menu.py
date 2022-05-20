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

        self.buttons = [Button('mbtn_new_game', draw_pos=(50, 220)),
                        Button('mbtn_continue', draw_pos=(537, 220)),
                        Button('mbtn_tutorial', draw_pos=(50, 390)),
                        Button('mbtn_ranking', draw_pos=(537, 390)),
                        Button('mbtn_quit', draw_pos=(537, 560))]

        super().__init__(draw_pos, background)

        self.current_game = None
        # self.init_buttons()
        self.menu_shown = True

        self.save_menu = SaveMenu(self.win)

    def get_window(self):
        return self.win

    def show_menu(self):
        self.menu_shown = True
        while self.menu_shown:
            self.win.blit(self.background, self.draw_pos)

            m_pos = pygame.mouse.get_pos()
            for button in self.buttons:
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
                        for button in self.buttons:
                            if button.click_check(m_pos):
                                button.button_down()
                if event.type == MOUSEBUTTONUP:
                    for button in self.buttons:
                        if button.click_check(m_pos) and button.pressed:
                            self.button_click(button)
                        button.button_up()

            # Redisplay
            pygame.display.update()

    def button_click(self, button):
        name = button.get_button_name()
        button.button_up()
        if name == 'mbtn_new_game':
            self.new_game_button_clicked()
        elif name == 'mbtn_continue':
            self.resume_game_button_clicked()
        elif name == 'mbtn_tutorial':
            self.tutorial_button_clicked()
        elif name == 'mbtn_scoreboard':
            self.scoreboard_button_clicked()
        elif name == 'mbtn_quit':
            self.end_game()
        else:
            print('No Button Clicked')

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

    def end_game(self):
        self.menu_shown = False
        exit(0)