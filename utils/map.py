import pygame


class Map:

    def __init__(self, map_nr):
        self.bg = pygame.image.load("assets/img/map/map-{}.png".format(map_nr)).convert_alpha()
        self.enemies = list()
        self.path = [(0, 57), (328, 184), (349, 186), (482, 157), (800, 99), (828, 109), (891, 199), (884, 231), (755, 382), (735, 396), (697, 389), (485, 314), (462, 314), (449, 335), (416, 437), (430, 457), (472, 462), (939, 503), (1022, 469)]

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
