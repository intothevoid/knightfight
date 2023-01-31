"""
The board class to capture the state of the chess board.
"""

import pygame
from chess.piece import Piece
from config import config


class Board:
    def __init__(self, window_surface: pygame.surface.Surface) -> None:
        board_size = config.APP_CONFIG["board"]["size"]
        board_image = config.APP_CONFIG["board"]["image"]

        self.window_surface = window_surface
        self.board_image = pygame.image.load(f"assets/{board_image}")
        self.board_rect = self.board_image.get_rect()
        self.board_rect.topleft = (0, 0)
        self.board_image = pygame.transform.scale(
            self.board_image, (board_size, board_size)
        )

        # maintain a list of pieces on the board
        self.pieces = []

    def render(self) -> None:
        self.window_surface.blit(self.board_image, self.board_rect)
