import pygame


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

            # Redisplay

