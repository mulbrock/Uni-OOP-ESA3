import pygame
from pygame.locals import *

from menus.menu import Menu
from menus.buttons.button import Button


class IngameMenu(Menu):

    def __init__(self, draw_pos=(0, 0)):
        bg = pygame.image.load("assets/img/menu/menu.png").convert_alpha()
        super().__init__(draw_pos, bg)
        self.size = bg.get_size()

    def set_draw_pos(self, pos):
        self.draw_pos = pos

    def click_check(self, pos):
        x, y = pos

        x1, y1 = self.draw_pos
        x2, y2 = x1 + (self.size[0]), y1 + (self.size[1])

        if x1 <= x <= x2:
            if y1 <= y <= y2:
                return True

    def get_symbol(self):
        return self.background

    def get_height(self):
        return self.size[1]

    def get_width(self):
        return self.size[0]
