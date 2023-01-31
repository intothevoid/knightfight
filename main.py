"""
Knight Fight is a Chess game written using pygame.
"""

import pygame
import sys

from chess.board import Board
from config import config

BOARD_BK_COLOUR = (255, 255, 255)

if __name__ == "__main__":
    # initialize pygame and load config
    pygame.init()
    config.read_config()

    # set up the window
    board_size = config.APP_CONFIG["board"]["size"]
    screen = pygame.display.set_mode((board_size, board_size))
    screen.fill(BOARD_BK_COLOUR)
    pygame.display.set_caption("Knight Fight")
    pygame.mouse.set_visible(1)

    # render the board
    board = Board(screen)
    board.render()

    # main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
