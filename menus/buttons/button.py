import pygame


class Button:

    def __init__(self, button_name, draw_pos=(0, 0)):
        self.button_name = button_name
        self.symbol = pygame.image.load("assets/img/buttons/{}.png".format(button_name)).convert_alpha()
        self.unpressed_symbol = pygame.image.load("assets/img/buttons/{}.png".format(button_name)).convert_alpha()
        self.pressed_symbol = pygame.image.load("assets/img/buttons/{}_pressed.png".format(button_name)).convert_alpha()
        self.size = self.symbol.get_size()
        self.draw_pos = draw_pos

    def click(self):
        raise NotImplementedError

    def get_button_name(self):
        return self.button_name

    def get_symbol(self):
        return self.symbol

    def set_symbol(self, button_name):
        self.symbol = pygame.image.load("assets/img/buttons/{}_pressed.png".format(button_name)).convert_alpha()

    def get_draw_pos(self):
        return self.draw_pos

    def set_draw_pos(self, pos):
        self.draw_pos = pos

    def click_check(self, pos):
        x, y = pos

        x1, y1 = self.draw_pos
        x2, y2 = x1 + (self.size[0]), y1 + (self.size[1])

        if x1 <= x <= x2:
            if y1 <= y <= y2:
                return True

    def get_height(self):
        return self.size[1]

    def button_down(self):
        self.symbol = self.pressed_symbol

    def button_up(self):
        self.symbol = self.unpressed_symbol