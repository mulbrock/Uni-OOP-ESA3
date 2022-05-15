import pygame
import math
from entities.towers.tower import Tower


class LaserTower(Tower):

    def __init__(self, pos: tuple):
        _symbol = pygame.image.load("assets/img/towers/laser_1.png")
        _range = 100
        _cool_down = 5.0
        super().__init__(pos, _symbol, _range, _cool_down)
