from abc import ABC
import pygame


class Entity(ABC):

    def __init__(self, _size: tuple, pos: tuple, _symbol: pygame.image):
        self.size = _size
        self.position = pos
        self.symbol = _symbol
        x, y = pos
        self.center = x + (self.size[0]/2), y + (self.size[1]/2)

    def set_symbol(self, path):
        self.symbol = pygame.image.load(path).convert_alpha()
        self.size = self.symbol.get_size()

    def get_symbol(self):
        return self.symbol

    def get_center(self):
        return self.center

    def get_pos(self):
        return self.position
