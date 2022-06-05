import pygame
from pygame.locals import *
from menus.buttons.button import Button
from menus.buttons.char_button import CharButton

class GameOver:

    def __init__(self, win, main_menu, bg, score):
        self.win = win
        self.howto_shown = False
        self.main_menu = main_menu
        self.score = score
        self.game_over_shown = True

        self.background = bg
        self.overlay = self.game_over_overlay = pygame.image.load\
            ("assets/img/game_over.png").convert_alpha()

        self.backspace_button = Button('ebtn_backspace',
                                       draw_pos=(837, 350))
        self.enter_button = Button('ebtn_enter', draw_pos=(767, 560),
                                   inactive=True)

        self.char_buttons = [
            CharButton('1', 'ebtn_1', draw_pos=(137, 350)),
            CharButton('2', 'ebtn_2', draw_pos=(207, 350)),
            CharButton('3', 'ebtn_3', draw_pos=(277, 350)),
            CharButton('4', 'ebtn_4', draw_pos=(347, 350)),
            CharButton('5', 'ebtn_5', draw_pos=(417, 350)),
            CharButton('6', 'ebtn_6', draw_pos=(487, 350)),
            CharButton('7', 'ebtn_7', draw_pos=(557, 350)),
            CharButton('8', 'ebtn_8', draw_pos=(627, 350)),
            CharButton('9', 'ebtn_9', draw_pos=(697, 350)),
            CharButton('0', 'ebtn_0', draw_pos=(767, 350)),
            CharButton('Q', 'ebtn_q', draw_pos=(137, 420)),
            CharButton('W', 'ebtn_w', draw_pos=(207, 420)),
            CharButton('E', 'ebtn_e', draw_pos=(277, 420)),
            CharButton('R', 'ebtn_r', draw_pos=(347, 420)),
            CharButton('T', 'ebtn_t', draw_pos=(417, 420)),
            CharButton('Z', 'ebtn_z', draw_pos=(487, 420)),
            CharButton('U', 'ebtn_u', draw_pos=(557, 420)),
            CharButton('I', 'ebtn_i', draw_pos=(627, 420)),
            CharButton('O', 'ebtn_o', draw_pos=(697, 420)),
            CharButton('P', 'ebtn_p', draw_pos=(767, 420)),
            CharButton('A', 'ebtn_a', draw_pos=(137, 490)),
            CharButton('S', 'ebtn_s', draw_pos=(207, 490)),
            CharButton('D', 'ebtn_d', draw_pos=(277, 490)),
            CharButton('F', 'ebtn_f', draw_pos=(347, 490)),
            CharButton('G', 'ebtn_g', draw_pos=(417, 490)),
            CharButton('H', 'ebtn_h', draw_pos=(487, 490)),
            CharButton('J', 'ebtn_j', draw_pos=(557, 490)),
            CharButton('K', 'ebtn_k', draw_pos=(627, 490)),
            CharButton('L', 'ebtn_l', draw_pos=(697, 490)),
            CharButton('Y', 'ebtn_y', draw_pos=(277, 560)),
            CharButton('X', 'ebtn_x', draw_pos=(347, 560)),
            CharButton('C', 'ebtn_c', draw_pos=(417, 560)),
            CharButton('V', 'ebtn_v', draw_pos=(487, 560)),
            CharButton('B', 'ebtn_b', draw_pos=(557, 560)),
            CharButton('N', 'ebtn_n', draw_pos=(627, 560)),
            CharButton('M', 'ebtn_m', draw_pos=(697, 560))
        ]

        self.player_name = ""

    def show_game_over(self):
        while self.game_over_shown:
            self.win.blit(self.background, (0, 0))
            self.win.blit(self.game_over_overlay, (0, 0))

            self.win.blit(self.backspace_button.get_symbol(),
                          self.backspace_button.get_draw_pos())
            self.win.blit(self.enter_button.get_symbol(),
                          self.enter_button.get_draw_pos())
            for char_button in self.char_buttons:
                self.win.blit(char_button.get_symbol(),
                              char_button.get_draw_pos())

            player_name_font = pygame.font.Font("assets/orbitron-black.otf",
                                                40)
            player_name_font = player_name_font.render(self.player_name,
                                                       True, (0, 0, 0))
            self.win.blit(player_name_font, (430, 677))

            m_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit(0)

                if event.type == MOUSEBUTTONDOWN:
                    left, middle, right = pygame.mouse.get_pressed()
                    if left:
                        if self.backspace_button.click_check(m_pos):
                            self.backspace_button.button_down()
                        elif self.enter_button.click_check(m_pos):
                            self.enter_button.button_down()
                        else:
                            for char_button in self.char_buttons:
                                if char_button.click_check(m_pos):
                                    char_button.button_down()
                                    break
                if event.type == MOUSEBUTTONUP:
                    if self.backspace_button.click_check(m_pos) and \
                            self.backspace_button.pressed:
                        self.backspace_button.button_up()
                        self.delete_char()
                    elif self.enter_button.click_check(m_pos) and \
                            self.enter_button.pressed:
                        self.enter()
                        self.main_menu.show_menu()
                    else:
                        for char_button in self.char_buttons:
                            if char_button.click_check(m_pos) and \
                                    char_button.pressed:
                                self.add_char(char_button.get_char())
                                char_button.button_up()
                                break

                    for char_button in self.char_buttons:
                        char_button.button_up()
                    self.backspace_button.button_up()
                    self.enter_button.button_up()

            pygame.display.update()

    def add_char(self, char):
        if len(self.player_name) == 0:
            self.enter_button.activate()
        if len(self.player_name) < 5:
            self.player_name += char
        if len(self.player_name) == 5:
            for char_button in self.char_buttons:
                char_button.deactivate()

    def delete_char(self):
        if len(self.player_name) > 0:
            self.player_name = self.player_name[:-1]
            for char_button in self.char_buttons:
                char_button.activate()
        if len(self.player_name) == 0:
            self.enter_button.deactivate()

    def enter(self):
        self.main_menu.leaderboard.update_leaderboard(self.player_name,
                                                      self.score)
        self.main_menu.game_over()