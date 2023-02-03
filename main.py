"""
Knight Fight is a Chess game written using pygame.
"""

import pygame
import sys

from chess.board import Board
from config import config

BOARD_BK_COLOUR = (255, 255, 255)


class KnightFight:
    def __init__(self):
        self.dragged_piece = None
        self.drag_offset = None

    def run(self):
        # initialize pygame and load config
        pygame.init()
        config.read_config()

        # set up the window
        board_size = config.APP_CONFIG["board"]["size"]
        screen = pygame.display.set_mode((board_size, board_size))
        screen.fill(BOARD_BK_COLOUR)
        pygame.display.set_caption(
            "Knight Fight - https://github.com/intothevoid/knightfight"
        )
        pygame.mouse.set_visible(True)

        # setup board
        board = Board(screen)

        # main loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # check if a piece is clicked
                    pos = pygame.mouse.get_pos()
                    clicked_piece = board.get_piece_at(pos)[0]  # only one piece
                    if clicked_piece:
                        # save starting position and start drag-drop event
                        self.dragged_piece = clicked_piece
                        self.drag_offset = (
                            pos[0] - clicked_piece.piece_rect.x,
                            pos[1] - clicked_piece.piece_rect.y,
                        )
                elif event.type == pygame.MOUSEMOTION:
                    # update piece position if drag drop is active
                    if self.dragged_piece:
                        pos = pygame.mouse.get_pos()
                        if self.drag_offset:
                            self.dragged_piece.piece_rect.x = (
                                pos[0] - self.drag_offset[0]
                            )
                            self.dragged_piece.piece_rect.y = (
                                pos[1] - self.drag_offset[1]
                            )
                elif event.type == pygame.MOUSEBUTTONUP:
                    # end drag and drop event
                    if self.dragged_piece:
                        # update piece position on board
                        pos = pygame.mouse.get_pos()
                        board.move_piece(self.dragged_piece, pos)
                        self.dragged_piece = None
                        self.drag_offset = None

            # update the display
            board.render()
            pygame.display.update()


if __name__ == "__main__":
    chess = KnightFight()
    chess.run()
