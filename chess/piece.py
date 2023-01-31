"""
The piece class to capture the state of the chess pieces.
"""

import pygame
from chess.types import PieceType, PieceColour


class Piece:
    def __init__(
        self,
        window_surface,
        piece_type: PieceType,
        piece_colour: PieceColour,
        piece_pos,
    ) -> None:
        self.window_surface = window_surface
        self.piece_type = piece_type
        self.piece_colour = piece_colour
        self.piece_pos = piece_pos
        self.piece_image = pygame.image.load(f"assets/{piece_colour}_{piece_type}.png")
        self.piece_rect = self.piece_image.get_rect()
        self.piece_rect.topleft = piece_pos
        self.piece_image = pygame.transform.scale(self.piece_image, (100, 100))

    def render(self) -> None:
        self.window_surface.blit(self.piece_image, self.piece_rect)
