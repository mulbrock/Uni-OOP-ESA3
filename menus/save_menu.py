import pygame
from menus.menu import Menu


class SaveMenu(Menu):

    def __init__(self, win):
        self.win = win
        background = pygame.image.load("assets/img/menu/menu.png").convert_alpha()
        self.draw_pos = (self.win.get_width() / 2) - (background.get_width() / 2), \
                        (self.win.get_height() / 2) - (background.get_height() / 2)
        super().__init__(self.draw_pos, background)

    def draw(self):
        self.win.blit(self.background, self.draw_pos)


