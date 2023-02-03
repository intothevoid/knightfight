"""
Knight Fight is a Chess game written using pygame.
"""

import pygame
import sys

from chess.board import Board
from config import config
from chess.types import PieceColour
from helpers.log import LOGGER
from sound.playback import play_music

BOARD_BK_COLOUR = (255, 255, 255)


class KnightFight:
    def __init__(self):
        self.dragged_piece = None
        self.drag_offset = None

    def show_splash_screen(self, screen):
        """
        Show splash screen on new window
        """
        # load splash screen image
        splash_image = pygame.image.load("assets/logo.png")

        # set image size to 50% of board size
        splash_image = pygame.transform.scale(
            splash_image,
            (
                config.APP_CONFIG["board"]["size"],
                config.APP_CONFIG["board"]["size"],
            ),
        )

        splash_rect = splash_image.get_rect()
        splash_rect.center = (
            config.APP_CONFIG["board"]["size"] // 2,
            config.APP_CONFIG["board"]["size"] // 2,
        )

        # show splash screen
        screen.blit(splash_image, splash_rect)
        pygame.display.update()

        # show splash screen for 3 seconds
        pygame.time.delay(3000)

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

        # show splash screen
        # self.show_splash_screen(screen)

        # setup board
        board = Board(screen)

        # track turn
        turn = PieceColour.White

        # play music
        if config.APP_CONFIG["game"]["music"]:
            ost = config.APP_CONFIG["game"]["soundtrack"]
            play_music(ost)

        try:
            # main loop
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # check if a piece is clicked
                        pos = pygame.mouse.get_pos()
                        try:
                            clicked_piece = board.get_piece_at(pos)[0]  # only one piece
                            if clicked_piece and clicked_piece.piece_colour == turn:
                                # save starting position and start drag-drop event
                                self.dragged_piece = clicked_piece
                                self.drag_offset = (
                                    pos[0] - clicked_piece.piece_rect.x,
                                    pos[1] - clicked_piece.piece_rect.y,
                                )
                        except IndexError:
                            # no piece at position
                            pass
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
                            original_pos = self.dragged_piece.grid_pos
                            pos = pygame.mouse.get_pos()
                            piece_moved = board.move_piece(self.dragged_piece, pos)
                            moved_pos = self.dragged_piece.grid_pos
                            self.dragged_piece = None
                            self.drag_offset = None

                            if piece_moved and original_pos != moved_pos:
                                # change turn
                                turn = (
                                    PieceColour.White
                                    if turn == PieceColour.Black
                                    else PieceColour.Black
                                )

                # update the display
                board.render()
                pygame.display.update()

        except Exception as exc:
            LOGGER.error(exc)


if __name__ == "__main__":
    chess = KnightFight()
    chess.run()
