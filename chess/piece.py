"""
The piece class to capture the state of the chess pieces.
"""

import pygame
from chess.types import PieceType, PieceColour
from config import config


def get_piece_from_strip(image_file: str,
                         piece_type: PieceType) -> pygame.Surface:

    strip_image = pygame.image.load(f"assets/{image_file}")
    piece_width = int(strip_image.get_width() / 6)
    piece_height = int(strip_image.get_height())

    # Get the index of the desired piece in the strip
    piece_index = {"pawn": 0, "knight": 1, "rook": 2,
                   "bishop": 3, "queen": 4, "king": 5}[piece_type.lower()]
    piece_x = piece_width * piece_index

    # Create a new surface to store the desired piece
    piece_image = pygame.Surface(
        (piece_width, piece_height), pygame.SRCALPHA)

    piece_image.blit(strip_image, (0, 0), (piece_x, 0,
                     piece_width, piece_height))

    # create mask for transparent background
    piece_mask = pygame.mask.from_surface(piece_image)

    return piece_image, piece_mask


class Piece:
    def __init__(
        self,
        window_surface,
        piece_type: PieceType,
        piece_colour: PieceColour,
        piece_pos,
    ) -> None:
        size_x = config.APP_CONFIG["piece"]["size_x"]
        size_y = config.APP_CONFIG["piece"]["size_y"]
        self.window_surface = window_surface
        self.piece_type = piece_type
        self.piece_colour = piece_colour
        self.piece_pos = piece_pos

        if piece_colour == PieceColour.White:
            self.piece_image, _ = get_piece_from_strip(
                config.APP_CONFIG["board"]["white_pieces"], piece_type)
        else:
            self.piece_image, _ = get_piece_from_strip(
                config.APP_CONFIG["board"]["black_pieces"], piece_type)

        self.piece_image = pygame.transform.scale(
            self.piece_image, (size_x, size_y))

        self.piece_rect = self.piece_image.get_rect()
        self.piece_rect.topleft = piece_pos

    def render(self) -> None:
        self.window_surface.blit(self.piece_image, self.piece_rect)
