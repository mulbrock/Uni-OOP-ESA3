import pygame
from pygame.locals import *

from utils.map import Map
from entities.enemies.enemy_one import EnemyOne


class Game:

    def start(self):
        pygame.init()

        # Display config
        win = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption("Tower Defense")

        # Entities
        game_map = Map("01")
        bg = game_map.get_bg()
        en = EnemyOne(game_map.get_path())
        game_map.add_enemy(en)

        # Action --> ALTER
        # Assign variables
        keep_going = True
        clock = pygame.time.Clock()

        path = list()

        # Loop
        while keep_going:

            # Timer
            clock.tick(90)
            win.blit(bg, (0, 0))

            # Event handling
            m_pos = pygame.mouse.get_pos()
            area = game_map.click_check(m_pos)
            if area is not None:
                win.blit(area["image"], area["A"])

            for event in pygame.event.get():
                if event.type == QUIT:
                    keep_going = False
                    break
                if event.type == MOUSEBUTTONDOWN:
                    print("click")

            for enemy in game_map.get_enemies():
                win.blit(enemy.get_symbol(), enemy.get_center())
                if not enemy.move_forward():
                    game_map.remove_enemy(enemy)

            # Redisplay
            pygame.display.update()
