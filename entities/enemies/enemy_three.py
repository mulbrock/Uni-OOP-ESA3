from entities.enemies.enemy import Enemy
import pygame


class EnemyThree(Enemy):

    def __init__(self, _path):
        symbol_path = "assets/img/enemies/enemy_3.png"
        hp = 10
        super().__init__(_path, hp, symbol_path)
