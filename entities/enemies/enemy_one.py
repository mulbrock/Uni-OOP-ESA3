import pygame
from entities.enemies.enemy import Enemy


class EnemyOne(Enemy):

    def __init__(self, _path):
        symbol = pygame.image.load("assets/img/enemies/enemy_1.png")
        hp = 5
        super().__init__(_path, hp, symbol)

