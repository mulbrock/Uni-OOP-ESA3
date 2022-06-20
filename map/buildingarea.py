import pygame.image
from entities.towers.tower import Tower


class BuildingArea:
    """
    Das Gebiet, in dem Gebaut werden kann.
    """

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
        self.image = pygame.image.load("assets/img/map/building_area_{}.png".
                                       format(area_number)).convert_alpha()
        self.buildings = list()

    def is_point_in_building_area(self, pos):
        """
        Überprüft, ob der Punkt in der Building area ist.
        :param pos: tupel: int
        :return: boolean
        """
        return self.is_point_in_area(pos, self.area)

    def is_tower_in_building_area(self, tower: Tower):
        """
        Überprüft, ob der Turm in der Building area ist.
        :param tower: Tower
        :return: boolean
        """
        area = tower.get_area()
        x1, y1 = area["A"]
        x2, y2 = area["C"]

        if self.is_point_in_building_area((x1, y1)) and \
                self.is_point_in_building_area((x2, y2)):
            return True
        return False

    def is_point_in_area(self, point, area):
        """
        Überprüft, ob der Punkt in der area ist.
        :param point, area: tupel: int, area: dict
        :return: boolean
        """
        x, y = point

        xA, yA = area["A"]
        xB, yB = area["B"]
        xC, yA = area["C"]
        xD, yD = area["D"]

        if xA <= x <= xC:
            if yD <= y <= yB:
                return True

    def is_building_space_empty(self, tower_to_build: Tower):
        """
        Überprüft, ob der beanspruchte Bauplatz frei ist.
        :param tower_to_build: Tower
        :return: boolean
        """
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

    def add_building(self, tower: Tower, m_pos: tuple):
        """
        Fügt einen Turm zu einer Building area hinzu.
        :param tower: Tower
        :param m_pos: tuple: int
        :return:
        """
        tower.set_center(m_pos)
        self.buildings.append(tower)

    def get_image(self):
        """
        Liefert das Bild der Area.
        :return: pygame.image
        """
        return self.image

    def get_a(self):
        """
        Liefert den Punkt A.
        :return:
        """
        return self.A

    def get_buildings(self):
        """
        Liefert eine List der Gebäude in der Area.
        :return: list: Tower
        """
        return self.buildings

    def has_tower(self, tower):
        """
        Überprüft, ob Turm in der Building area ist.
        :param tower: Tower
        :return: boolean
        """
        for t in self.buildings:
            if t == tower:
                return True

    def remove_tower(self, tower):
        """
        Entfernt einen Turm aus der Building area.
        :param tower: Tower
        :return:
        """
        self.buildings.remove(tower)

    def hover_check(self, pos):
        """
        Überprüft, ob Mausposition in der Buildingarea ist.
        :param pos: tuple: int
        :return: boolean
        """
        return self.is_point_in_building_area(pos)
