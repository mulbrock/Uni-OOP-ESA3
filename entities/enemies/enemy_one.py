import pygame
from entities.enemies.enemy import Enemy


class EnemyOne(Enemy):

    def __init__(self, _size: tuple, pos: tuple, _path, _hp):
        symbol = pygame.image.load("assets/img/enemies/enemy-01.png")
        super().__init__(_size, pos, _path, _hp, symbol)

