import pygame.image


class BuildingArea:

    def __init__(self, area_number, _a, _b, _c, _d):
        self.A = _a
        self.B = _b
        self.C = _c
        self.D = _d
        self.image = pygame.image.load("assets/img/map/building_area_{}.png".format(area_number)).convert_alpha()
        self.buildings = dict()

    def is_building_area(self, pos):
        x, y = pos

        if self.A[0] <= x <= self.C[0]:
            if self.A[1] <= y <= self.C[1]:
                return True
        return False

    def add_building(self, building):
        self.buildings[building.id] = building

    def get_image(self):
        return self.image

    def get_a(self):
        return self.A
