from menus.buttons.button import Button

class CharButton(Button):

    def __init__(self, char, button_name, draw_pos=(0, 0), inactive=False):
        self.char = char
        super().__init__(button_name, draw_pos, inactive)

    def get_char(self):
        """
        Gibt das gespeicherte Schriftzeichen zurück.
        :return: self.char
        """
        return self.char