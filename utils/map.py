import pygame
from utils.buildingarea import BuildingArea

class Map:

    def __init__(self, map_nr):
        self.bg = pygame.image.load("assets/img/map/map-{}.png".format(map_nr)).convert_alpha()
        self.enemies = list()
        # ToDo: Path needs go be injected, depending on map that's being load
        self.path = [(0, 57), (328, 184), (349, 186), (482, 157), (800, 99), (828, 109), (891, 199), (884, 231), (755, 382), (735, 396), (697, 389), (485, 314), (462, 314), (449, 335), (416, 437), (430, 457), (472, 462), (939, 503), (1022, 469)]
        area_one = BuildingArea(1, (12, 149), (12, 224), (162, 224), (162, 149))
        area_two = BuildingArea(2, (279, 56), (279, 131), (479, 131), (479, 56))
        self.building_areas = list()
        self.building_areas.append(area_one)
        self.building_areas.append(area_two)


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

    def hover_check(self, pos):
        for area in self.building_areas:
            if area.is_point_in_building_area(pos):
                return area
        return None

    def get_building_areas(self):
        return self.building_areas

    def get_all_towers(self):
        towers = list()
        for area in self.building_areas:
            l = area.get_buildings()
            towers.extend(l)
        return towers
