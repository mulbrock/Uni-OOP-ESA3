import pygame
from entities.enemies.enemy import Enemy


class EnemyOne(Enemy):

    def __init__(self, _path):
        symbol = pygame.image.load("assets/img/enemies/enemy-01.png")
        size = symbol.get_size()
        hp = 5
        super().__init__(size, _path, hp, symbol)

