import pygame


class Map:

    def __init__(self, map_nr):
        self.bg = pygame.image.load("assets/img/map/map-{}.png".format(map_nr)).convert_alpha()
        self.enemies = list()

    def get_bg(self):
        return self.bg

    def set_enemies(self, _enemies):
        self.enemies = _enemies

    def add_enemy(self, enemy):
        self.enemies.append(enemy)
