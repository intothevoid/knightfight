"""
Knight Fight is a Chess game written using pygame.
"""

import pygame
import sys

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    screen.fill((255, 255, 255))
    pygame.display.set_caption("Knight Fight")
    pygame.mouse.set_visible(1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
