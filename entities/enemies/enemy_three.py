from entities.enemies.enemy import Enemy
import pygame


class EnemyThree(Enemy):

    def __init__(self, _path):
        symbol = pygame.image.load("assets/img/enemies/enemy_3.png")
        hp = 10
        super().__init__(_path, hp, symbol)
