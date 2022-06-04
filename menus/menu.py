import pygame

class Menu:

    def __init__(self, draw_pos, bg: pygame.image):
        self.draw_pos = draw_pos
        self.background = bg

        self.vertical_padding = 25
        self.horizontal_padding = 25

    def calculate_vertical_btn_draw_pos(self, button, button_list):
        list_len = len(button_list)
        button_image = button.get_symbol()
        x = (self.background.get_width()/2) - button_image.get_width()/2
        y = (self.background.get_height()/2) - button_image.get_height()/2
        y = y + (self.vertical_padding * list_len) + (button_image.get_height() *
                                                      list_len)
        return x, y

    def get_vertical_padding(self):
        return self.vertical_padding

    def get_draw_pos(self):
        return self.draw_pos
