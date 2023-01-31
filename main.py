"""
Knight Fight is a Chess game written using pygame.
"""

import pygame
import sys

from chess.board import Board

BOARD_BK_COLOUR = (255, 255, 255)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    screen.fill(BOARD_BK_COLOUR)
    pygame.display.set_caption("Knight Fight")
    pygame.mouse.set_visible(1)

    # render the board
    board = Board(screen)
    board.render()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
