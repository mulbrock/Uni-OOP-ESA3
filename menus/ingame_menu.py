import pygame
from menus.menu import Menu
from menus.buttons.button import Button

class IngameMenu(Menu):

    def __init__(self):
        bg = pygame.image.load("assets/img/menu/menu.png").convert_alpha()
        super().__init__((12, 556), bg)
        self.size = bg.get_size()
        self.buttons = [Button('btn_laserbuild', draw_pos=(32, 576)),
                        Button('btn_bombbuild', draw_pos=(327, 576)),
                        Button('btn_destroy', draw_pos=(622, 576)),
                        Button('btn_pause', draw_pos=(917, 576))]
        self.upgrade_mode = False

    def left_btn_check(self, pos):
        """
        Vergleicht die übergene Position mit der Position des linken Ingame-Menu Buttons.
        :param pos:
        :return:
        """
        x, y = pos

        x1 = 32
        x2 = 307

        y1 = 576
        y2 = 696

        if x1 <= x <= x2 and y1 <= y <= y2:
            return True

    def middle_btn_check(self, pos):
        """
        Vergleicht die übergene Position mit der Position des mittleren Ingame-Menu Buttons.
        :param pos:
        :return:
        """
        x, y = pos

        x1 = 327
        x2 = 602

        y1 = 576
        y2 = 696

        if x1 <= x <= x2 and y1 <= y <= y2:
            return True

    def right_btn_check(self, pos):
        """
        Vergleicht die übergene Position mit der Position des rechten Ingame-Menu Buttons.
        :param pos:
        :return:
        """
        x, y = pos

        x1 = 622
        x2 = 897

        y1 = 576
        y2 = 696

        if x1 <= x <= x2 and y1 <= y <= y2:
            return True

    def pause_check(self, pos):
        """
        Vergleicht die übergene Position mit der Position des Pause-Menu Buttons.
        :param pos:
        :return:
        """
        x, y = pos

        x1 = 917
        x2 = 992

        y1 = 576
        y2 = 736

        if x1 <= x <= x2 and y1 <= y <= y2:
            return True

    def get_symbol(self):
        """
        Gibt die Ingame-Menu Grafik zurück.
        :return:
        """
        return self.background

    def get_buttons(self):
        """
        Gibt die Buttons des Ingame-Menu zurück.
        :return: self.buttons
        """
        return self.buttons

    def switch_to_upgrade_view(self):
        """
        Wechselt von der Bau-Ansicht zur Upgrade-Ansicht des ausgewählten Turms.
        :return:
        """
        self.upgrade_mode = True
        self.buttons.clear()
        self.buttons = [Button('btn_range', draw_pos=(32, 576)),
                        Button('btn_frequency', draw_pos=(327, 576)),
                        Button('btn_power', draw_pos=(622, 576)),
                        Button('btn_pause', draw_pos=(917, 576))]

    def switch_to_build_view(self):
        """
        Wechselt von der Upgrade-Ansicht zur Bau-Ansicht.
        :return:
        """
        self.upgrade_mode = False
        self.buttons.clear()
        self.buttons = [Button('btn_laserbuild', draw_pos=(32, 576)),
                        Button('btn_bombbuild', draw_pos=(327, 576)),
                        Button('btn_destroy', draw_pos=(622, 576)),
                        Button('btn_pause', draw_pos=(917, 576))]