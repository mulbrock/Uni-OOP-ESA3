import pygame.image

from entities.towers.tower import Tower



class BuildingArea:

    def __init__(self, area_number, _a, _b, _c, _d):
        self.number = area_number
        self.A = _a
        self.B = _b
        self.C = _c
        self.D = _d
        self.area = {
            "A": _a,
            "B": _b,
            "C": _c,
            "D": _d
        }
        self.image = pygame.image.load("assets/img/map/building_area_{}.png".format(area_number)).convert_alpha()
        self.buildings = list()

    def is_point_in_building_area(self, pos):
        return self.is_point_in_area(pos, self.area)

    def is_tower_in_building_area(self, tower: Tower):
        area = tower.get_area()
        x1, y1 = area["A"]
        x2, y2 = area["C"]

        if self.is_point_in_building_area((x1, y1)) and self.is_point_in_building_area((x2, y2)):
            return True
        return False

    def is_point_in_area(self, point, area):
        x, y = point

        xA, yA = area["A"]
        xB, yB = area["B"]
        xC, yA = area["C"]
        xD, yD = area["D"]

        if xA <= x <= xC:
            if yD <= y <= yB:
                return True

    def is_building_space_empty(self, tower_to_build: Tower):
        area = tower_to_build.get_area()
        a = area["A"]
        b = area["B"]
        c = area["C"]
        d = area["D"]

        if len(self.buildings) <= 0:
            return True

        for tower in self.buildings:
            if tower.is_pos_in_area(a):
                return False
            if tower.is_pos_in_area(b):
                return False
            if tower.is_pos_in_area(c):
                return False
            if tower.is_pos_in_area(d):
                return False

        return True

    def add_building(self, tower: Tower):
        self.buildings.append(tower)

    def get_image(self):
        return self.image

    def get_a(self):
        return self.A

    def get_buildings(self):
        return self.buildings

    def get_number(self):
        return self.number
