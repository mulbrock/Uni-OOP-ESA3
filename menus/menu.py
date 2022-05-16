import pygame


class Menu:

    def __init__(self, draw_pos, bg: pygame.image):
        self.draw_pos = draw_pos
        self.background = bg

        self.buttons = {}
        self.vertical_padding = 25
        self.horizontal_padding = 25

    def get_buttons(self):
        return self.buttons

    def add_button(self, button):
        self.buttons.update({button.get_button_name(): button})

    def calculate_vertical_btn_draw_pos(self, button):
        button_image = button.get_symbol()
        x = (self.background.get_width()/2) - button_image.get_width()/2
        y = (self.background.get_height()/2) - button_image.get_height()/2

        return x, y

    def get_vertical_padding(self):
        return self.vertical_padding
