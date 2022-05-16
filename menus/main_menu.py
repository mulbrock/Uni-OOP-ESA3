import pygame
from pygame.locals import *

from game import Game
from menus.menu import Menu
from menus.buttons.button import Button


class MainMenu(Menu):

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tower Defense")

        self.win = pygame.display.set_mode((1024, 768))
        background = pygame.image.load("assets/img/menu/menu.png").convert_alpha()

        draw_pos = (self.win.get_width()/2) - (background.get_width()/2), \
                   (self.win.get_height()/2) - (background.get_height()/2)

        super().__init__(draw_pos, background)

        self.current_game = None
        self.init_buttons()
        self.menu_shown = True

    def init_buttons(self):
        new_game_button = Button("btn_bombbuild")
        pos = self.calculate_vertical_btn_draw_pos(new_game_button)
        new_game_button.set_draw_pos(pos)
        new_game_button.click = lambda: self.new_game_button_clicked()
        self.add_button(new_game_button)

        resume_game_button = Button("btn_bombbuild_pressed")
        pos = self.calculate_vertical_btn_draw_pos(resume_game_button)
        newpos = pos[0], pos[1] + self.get_vertical_padding() + resume_game_button.get_height()
        resume_game_button.set_draw_pos(newpos)
        resume_game_button.click = lambda: self.resume_game_button_clicked()
        self.add_button(resume_game_button)

        save_game = Button("btn_frequency")
        pos = self.calculate_vertical_btn_draw_pos(save_game)
        newpos = pos[0], pos[1] + self.get_vertical_padding()*2 + save_game.get_height()*2
        save_game.set_draw_pos(newpos)
        save_game.click = lambda: self.save_game_clicked()
        self.add_button(save_game)

    def get_window(self):
        return self.win

    def show_menu(self):
        self.menu_shown = True
        while self.menu_shown:
           # self.win.blit(self.background, self.draw_pos)

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

    def save_game_clicked(self):
        print("save")

    def end_game(self):
        self.menu_shown = False
