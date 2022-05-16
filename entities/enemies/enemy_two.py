from entities.enemies.enemy import Enemy
import pygame


class EnemyTwo(Enemy):

    def __init__(self, _path):
        symbol = pygame.image.load("assets/img/enemies/enemy_2.png")
        hp = 10
        super().__init__(_path, hp, symbol)
