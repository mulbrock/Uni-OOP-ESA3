import pygame
from pygame.locals import *


class Game:

    def start(self):
        pygame.init()

        # Display config
        win = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption("Tower Defense")

        # Entities

        # Action --> ALTER
        # Assign variables
        keep_going = True
        clock = pygame.time.Clock()

        # Loop
        while keep_going:

            # Timer
            clock.tick(45)

            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    keep_going = False
                    break
                if event.type == MOUSEBUTTONDOWN:
                    print("MOUSE")

            # Redisplay
            pygame.display.update()

