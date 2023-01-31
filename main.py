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
        pygame.display.set_caption("Knight Fight")
        pygame.mouse.set_visible(1)

        # render the board
        board = Board(screen)
        board.render()

        # main loop
        while True:
            # grab initial position
            pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # check if a piece is clicked
                    pos = pygame.mouse.get_pos()
                    clicked_piece = board.get_piece_at(pos)

                    if clicked_piece:
                        # save starting position and start drag-drop event
                        self.dragged_piece = clicked_piece
                        self.drag_offset = (pos[0] - clicked_piece.piece_rect.x,
                                            pos[1] - clicked_piece.piece_rect.y)
                elif event.type == pygame.MOUSEMOTION:
                    # update piece position if drag drop is active
                    if self.dragged_piece:
                        pos = pygame.mouse.get_pos()
                        self.dragged_piece.piece_rect.x = pos[0] - \
                            self.drag_offset[0]
                        self.dragged_piece.piece_rect.y = pos[1] - \
                            self.drag_offset[1]
                elif event.type == pygame.MOUSEBUTTONUP:
                    # end drag and drop event
                    if self.dragged_piece:
                        # update piece position on board
                        pos = pygame.mouse.get_pos()
                        self.dragged_piece.move_to(board.get_grid_at(pos))
                        self.dragged_piece = None
                        self.drag_offset = None

            board.render()
            pygame.display.update()


if __name__ == "__main__":
    chess = KnightFight()
    chess.run()
