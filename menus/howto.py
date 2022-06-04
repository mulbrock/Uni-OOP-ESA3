import pygame
from pygame.locals import *
from menus.menu import Menu
from menus.buttons.button import Button

class Howto(Menu):

    def __init__(self, win, main_menu):
        self.win = win
        self.howto_shown = False
        self.main_menu = main_menu

        self.back_button = Button('lbtn_back', draw_pos=(814, 50))

        background = pygame.image.load("assets/img/menu/howto.png").convert_alpha()
        draw_pos = (0, 0)
        super().__init__(draw_pos, background)

    def show_howto(self):
        self.howto_shown = True
        while self.howto_shown:
            self.win.blit(self.background, self.draw_pos)
            self.win.blit(self.back_button.get_symbol(),
                          self.back_button.get_draw_pos())

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
                        self.howto_shown = False
                        self.main_menu.show_menu()
                    else:
                        self.back_button.button_up()

            pygame.display.update()