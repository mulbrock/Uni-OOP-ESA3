from abc import ABC
import pygame


class Entity(ABC):

    def __init__(self, _size: tuple, pos: tuple, _symbol: pygame.image):
        self.size = _size
        self.position = pos
        self.symbol = _symbol
        self.center = (0, 0)
        self.set_center(pos)

    def set_symbol(self, path):
        self.symbol = pygame.image.load(path).convert_alpha()
        self.size = self.symbol.get_size()

    def get_symbol(self):
        return self.symbol

    def get_center(self):
        return self.center

    def set_center(self, pos):
        x, y = pos
        self.center = x + (self.size[0] / 2), y + (self.size[1] / 2)

    def get_pos(self):
        return self.position

    def set_pos(self, _pos):
        self.position = _pos
        self.set_center(_pos)

