import pygame

class Menu:

    def __init__(self, draw_pos, bg: pygame.image):
        self.draw_pos = draw_pos
        self.background = bg

    def get_draw_pos(self):
        """
        Gibt die Zeichenposition des Menu zurück.
        :return: self.draw_pos
        """
        return self.draw_pos
