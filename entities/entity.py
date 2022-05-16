from abc import ABC
import pygame


class Entity(ABC):

    def __init__(self, _pos: tuple, _symbol: pygame.image):
        self.size = _symbol.get_size()
        self.symbol = _symbol
        self.center = _pos
        self.draw_pos = self.center[0] - self.size[0] / 2, self.center[1] - self.size[1] / 2

        self.area = {}
        self.set_area()

    def set_symbol(self, path):
        self.symbol = pygame.image.load(path).convert_alpha()
        self.size = self.symbol.get_size()
        self.set_area()

    def get_symbol(self):
        return self.symbol

    def get_draw_pos(self):
        return self.draw_pos

    def get_size(self):
        return self.size

    def get_center(self):
        return self.center

    def set_center(self, center_pos):
        self.center = center_pos
        self.draw_pos = self.center[0] - self.size[0] / 2, self.center[1] - self.size[1] / 2

    def is_pos_in_area(self, pos):
        x, y = pos

        x1, y1 = self.center[0] - self.size[0] / 2, self.center[1] - self.size[1] / 2
        x2, y2 = x1 + (self.size[0]), y1 + (self.size[1])

        if x1 <= x <= x2:
            if y1 <= y <= y2:
                return True

    def click_check(self, pos):
        return self.is_pos_in_area(pos)

    def get_area(self):
        return self.area

    def set_area(self):
        a = self.center[0] - self.size[0] / 2, self.center[1] - self.size[1] / 2
        b = self.center[0] + self.size[0] / 2, self.center[1] - self.size[1] / 2
        c = self.center[0] + self.size[0] / 2, self.center[1] + self.size[1] / 2
        d = self.center[0] - self.size[0] / 2, self.center[1] + self.size[1] / 2

        self.area = {
            "A": a,
            "B": b,
            "C": c,
            "D": d
        }
