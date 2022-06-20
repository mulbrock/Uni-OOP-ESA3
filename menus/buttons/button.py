import pygame

class Button:

    def __init__(self, button_name, draw_pos=(0, 0), inactive=False):
        self.button_name = button_name
        self.symbol = pygame.image.load("assets/img/buttons/{}.png".
                                        format(button_name)).convert_alpha()
        self.unpressed_symbol = pygame.image.load("assets/img/buttons/{}.png".
                                                  format(button_name)).convert_alpha()
        self.pressed_symbol = pygame.image.load("assets/img/buttons/{}_pressed.png".
                                                format(button_name)).convert_alpha()
        self.size = self.symbol.get_size()
        self.draw_pos = draw_pos
        self.pressed = False
        self.inactive = inactive
        if self.inactive:
            self.deactivate()

    def activate(self):
        """
        Aktiviert den Button und stellt ihn normal dar.
        :return:
        """
        self.inactive = False
        self.symbol = pygame.image.load("assets/img/buttons/{}.png".
                                        format(self.button_name)).convert_alpha()

    def deactivate(self):
        """Deaktiviert den Button und stellt ihn ausgegraut dar."""
        self.inactive = True
        self.symbol = pygame.image.load("assets/img/buttons/{}_inactive.png".
                                        format(self.button_name)).convert_alpha()

    def get_button_name(self):
        """
        Gibt den Namen des Buttons zurück.
        :return: self.button_name
        """
        return self.button_name

    def get_symbol(self):
        """
        Gibt die Grafik des Buttons zurück.
        :return: self.symbol
        """
        return self.symbol

    def get_draw_pos(self):
        """
        Gibt die Zeichenposition des Buttons zurück.
        :return: self.draw_pos
        """
        return self.draw_pos

    def click_check(self, pos):
        """
        Vergleicht die übergebene Position mit der eigenen Area.
        :param pos:
        :return:
        """
        x, y = pos

        x1, y1 = self.draw_pos
        x2, y2 = x1 + (self.size[0]), y1 + (self.size[1])

        if x1 <= x <= x2:
            if y1 <= y <= y2:
                return True

    def button_down(self):
        """Stellt den Button als gedrückt dar."""
        if not self.inactive:
            self.symbol = self.pressed_symbol
            self.pressed = True

    def button_up(self):
        """
        Stellt den Button als ungedrückt dar.
        :return:
        """
        if not self.inactive:
            self.symbol = self.unpressed_symbol
            self.pressed = False