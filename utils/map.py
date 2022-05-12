import pygame


class Map:

    def __init__(self, map_nr):
        self.bg = pygame.image.load("assets/img/map/map-{}.png".format(map_nr)).convert_alpha()
        self.path = [(0, 59), (325, 183), (361, 185), (798, 99), (824, 105), (883, 192), (891, 212), (873, 247), (744, 390), (729, 394), (486, 319), (458, 321), (419, 451), (452, 464), (930, 504), (1022, 469)]
        self.enemies = list()

    def get_bg(self):
        return self.bg

    def set_enemies(self, _enemies):
        self.enemies = _enemies

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def get_enemies(self):
        return self.enemies

    def remove_enemy(self, enemy):
        self.enemies.remove(enemy)

    def get_path(self):
        return self.path
