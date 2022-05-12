import pygame.image


class BuildingArea:

    def __init__(self, map_nr):
        self.areas = list()
        area_one = {
            "A": (12, 149),
            "B": (12, 224),
            "C": (162, 224),
            "D": (162, 149),
            "image": pygame.image.load("assets/img/map/building_area_1.png").convert_alpha()
        }
        area_two = {
            "A": (279, 56),
            "B": (279, 131),
            "C": (479, 131),
            "D": (479, 56),
            "image": pygame.image.load("assets/img/map/building_area_2.png").convert_alpha()
        }
        self.areas.append(area_one)
        self.areas.append(area_two)

    def get_areas(self):
        return self.areas

    def get_building_area(self, pos):
        x, y = pos

        for area in self.areas:
            if area["A"][0] <= x <= area["C"][0]:
                if area["A"][1] <= y <= area["B"][1]:
                    return area
        return None

    def is_building_area(self, pos):
        x, y = pos

        for area in self.areas:
            if area["A"][0] <= x <= area["C"][0]:
                if area["A"][1] <= y <= area["B"][1]:
                    return True
        return False
