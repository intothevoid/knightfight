"""
The board class to capture the state of the chess board.
"""

import pygame


class Board:
    def __init__(self, window_surface) -> None:
        self.window_surface = window_surface
        self.board_image = pygame.image.load("assets/board_plain_02.png")
        self.board_rect = self.board_image.get_rect()
        self.board_rect.topleft = (0, 0)
        self.board_image = pygame.transform.scale(self.board_image, (800, 800))

    def render(self) -> None:
        self.window_surface.blit(self.board_image, self.board_rect)
