from abc import ABC
import pygame


class Entity(ABC):
    """
    Allgemeine Entitiy-Klasse, Abstrakt, hat keine Instanzen.
    """

    def __init__(self, _pos: tuple, _symbol_path):
        self.symbol_path = _symbol_path
        self.symbol = pygame.image.load(_symbol_path).convert_alpha()
        self.size = self.symbol.get_size()
        self.center = _pos
        self.draw_pos = self.center[0] - self.size[0] / 2, self.center[1] - \
                        self.size[1] / 2

        self.area = {}
        self.set_area()

    def set_symbol_path(self, path):
        """
        Setzt den Pfad zum Bild des Entity
        :param path: str
        :return:
        """
        self.symbol_path = path
        self.symbol = pygame.image.load(path).convert_alpha()
        self.size = self.symbol.get_size()
        self.set_area()

    def get_symbol_path(self):
        """
        Liefert den aktuelle Pfad zum Bild.
        :return: path: str
        """
        return self.symbol_path

    def get_symbol(self):
        """
        Liefert das aktuelle Bild.
        :return: pygame.image
        """
        return self.symbol

    def get_draw_pos(self):
        """
        Liefert die aktuelle Position zurück, von der aus das Bild gezeichnet werden kann.
        :return: tupel: int
        """
        return self.draw_pos

    def get_size(self):
        """
        Liefert die Größe des Bildes.
        :return: tupel: int
        """
        return self.size

    def get_center(self):
        """
        Liefert das Zentrum des Bildes.
        :return: tupel: int
        """
        return self.center

    def set_center(self, center_pos):
        """
        Setzt das Zentrum der Entity und aktualisiert die draw-position und die Größe.
        :param center_pos: tupel: int
        :return:
        """
        self.center = center_pos
        self.draw_pos = self.center[0] - self.size[0] / 2, self.center[1] - \
                        self.size[1] / 2
        self.set_area()

    def is_pos_in_area(self, pos):
        """
        Überprüft, ob die Position innerhalb des Bildes liegt.
        :param pos: tupel: pos
        :return: boolean
        """
        x, y = pos

        x1, y1 = self.center[0] - self.size[0] / 2, self.center[1] - self.size[1] / 2
        x2, y2 = x1 + (self.size[0]), y1 + (self.size[1])

        if x1 <= x <= x2:
            if y1 <= y <= y2:
                return True

    def click_check(self, pos):
        """
        Überprüft, ob position in bild liegt.
        :param pos: tupel: int
        :return: boolean
        """
        return self.is_pos_in_area(pos)

    def get_area(self):
        """
        Liefert die aktuelle Area des Bildes
        :return: dict: A,B,C,D
        """
        return self.area

    def set_area(self):
        """
        Setzt die Area, abhängig vom Zentrum und der Größe des Bildes.
        :return:
        """
        a = self.center[0] - self.size[0] / 2, self.center[1] - self.size[1] / 2
        b = self.center[0] + self.size[0] / 2, self.center[1] - self.size[1] / 2
        c = self.center[0] + self.size[0] / 2, self.center[1] + self.size[1] / 2
        d = self.center[0] - self.size[0] / 2, self.center[1] + self.size[1] / 2

        self.area = {
            "A": a,
            "B": b,
            "C": c,
            "D": d
        }
