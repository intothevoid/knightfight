"""
The piece class to capture the state of the chess pieces.
"""

import pygame
from dataclasses import dataclass
from helpers.log import LOGGER
from typing import Tuple, Any
from config import config
from chess.converter import convert_grid_pos_to_algebraic_notation
from ai.movement import is_move_valid
from chess.state import BoardState, PieceColour, PieceType
from chess.types import GridPosition


def get_piece_from_strip(
    image_file: str, piece_type: PieceType
) -> Tuple[pygame.Surface, Any]:

    strip_image = pygame.image.load(f"assets/{image_file}")
    piece_width = int(strip_image.get_width() / 6)
    piece_height = int(strip_image.get_height())

    # Get the index of the desired piece in the strip
    piece_index = {
        "pawn": 0,
        "knight": 1,
        "rook": 2,
        "bishop": 3,
        "queen": 4,
        "king": 5,
    }[piece_type.value.lower()]
    piece_x = piece_width * piece_index

    # Create a new surface to store the desired piece
    piece_image = pygame.Surface((piece_width, piece_height), pygame.SRCALPHA)

    piece_image.blit(strip_image, (0, 0), (piece_x, 0, piece_width, piece_height))

    # create mask for transparent background
    piece_mask = pygame.mask.from_surface(piece_image)

    return piece_image, piece_mask


@dataclass
class Piece:
    def __init__(
        self,
        window_surface,
        piece_type: PieceType,
        piece_colour: PieceColour,
        piece_pos: Tuple[int, int],
        grid_pos: GridPosition,
    ) -> None:
        size_x = config.APP_CONFIG["piece"]["size_x"]
        size_y = config.APP_CONFIG["piece"]["size_y"]
        self.window_surface = window_surface
        self.piece_type = piece_type
        self.piece_colour = piece_colour
        self.piece_pos = piece_pos
        self.grid_pos = grid_pos

        if piece_colour == PieceColour.White:
            self.piece_image, _ = get_piece_from_strip(
                config.APP_CONFIG["board"]["white_pieces"], piece_type
            )
        else:
            self.piece_image, _ = get_piece_from_strip(
                config.APP_CONFIG["board"]["black_pieces"], piece_type
            )

        self.piece_image = pygame.transform.scale(self.piece_image, (size_x, size_y))

        self.piece_rect = self.piece_image.get_rect()
        self.piece_rect.topleft = piece_pos

    def __eq__(self, other):
        """
        Check if two pieces are equal
        """
        return (
            self.piece_type == other.piece_type
            and self.piece_colour == other.piece_colour
            and self.grid_pos == other.grid_pos
        )

    def move_to(self, new_grid_pos: GridPosition, board_state: BoardState):

        if new_grid_pos is None or new_grid_pos.row is None or new_grid_pos.col is None:
            return

        if new_grid_pos.row == -1 or new_grid_pos.col == -1:
            return

        # check if move is valid
        if not is_move_valid(
            self.grid_pos, new_grid_pos, self.piece_type, self.piece_colour, board_state
        ):
            # go back to old position
            self.piece_rect.topleft = (
                40 + self.grid_pos.col * 90,
                40 + self.grid_pos.row * 90,
            )
        else:
            LOGGER.debug(
                f"{self.piece_colour.value} {self.piece_type.value} moved {convert_grid_pos_to_algebraic_notation(self.grid_pos)} -> {convert_grid_pos_to_algebraic_notation(new_grid_pos)}"
            )

            self.grid_pos = new_grid_pos

            # margin is 40 pixels
            # each square is 90x90 pixels
            self.piece_rect.topleft = (
                40 + new_grid_pos.col * 90,
                40 + new_grid_pos.row * 90,
            )

    def render(self) -> None:
        # show grid if enabled in config
        if config.APP_CONFIG["game"]["show_grid"]:
            pygame.draw.rect(
                self.window_surface,
                (255, 0, 0),
                self.piece_rect,
                1,
            )

        # show grid position if enabled in config
        if config.APP_CONFIG["game"]["show_positions"]:
            font_name = config.APP_CONFIG["game"]["grid_font_name"]
            font_size = config.APP_CONFIG["game"]["grid_font_size"]
            grid_font = pygame.font.SysFont(font_name, font_size)
            grid_pos_text = grid_font.render(
                f"{self.grid_pos.row},{self.grid_pos.col}", True, (255, 0, 0)
            )
            self.window_surface.blit(
                grid_pos_text,
                (self.piece_rect.left + 5, self.piece_rect.top + 5),
            )
        self.window_surface.blit(self.piece_image, self.piece_rect)
