"""
The piece class to capture the state of the chess pieces.
"""

import pygame
import chess
from dataclasses import dataclass
from helpers.conversions import (
    grid_position_to_square,
    square_to_position,
    grid_pos_to_move,
)
from helpers.log import LOGGER
from typing import Tuple, Any
from config import config
from ai.validation import is_move_valid
from knightfight.state import BoardState, PieceColour, PieceType
from knightfight.types import GridPosition


def get_piece_from_strip(
    image_file: str, piece_type: PieceType
) -> Tuple[pygame.Surface, Any]:
    strip_image = pygame.image.load(f"assets/images/{image_file}")
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
        piece_pos_x: int,
        piece_pos_y: int,
        grid_pos: GridPosition,
        square: int,  # chess engine square
    ) -> None:
        size_x = config.APP_CONFIG["piece"]["size_x"]
        size_y = config.APP_CONFIG["piece"]["size_y"]
        self.window_surface = window_surface
        self.piece_type = piece_type
        self.piece_colour = piece_colour
        self.piece_pos_x = piece_pos_x
        self.piece_pos_y = piece_pos_y
        self.grid_pos = grid_pos
        self.square = square

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
        self.piece_rect.left = piece_pos_x
        self.piece_rect.top = piece_pos_y

    def __eq__(self, other):
        """
        Check if two pieces are equal
        """
        return (
            self.piece_type == other.piece_type
            and self.piece_colour == other.piece_colour
            and self.grid_pos == other.grid_pos
        )

    def move_to(
        self, new_grid_pos: GridPosition, board_state: BoardState, animate: bool = False
    ) -> bool:
        if new_grid_pos is None or new_grid_pos.row is None or new_grid_pos.col is None:
            return False

        if new_grid_pos.row == -1 or new_grid_pos.col == -1:
            return False

        # check if move is valid
        if not is_move_valid(
            self.grid_pos,
            new_grid_pos,
            board_state.engine_state,
        ):
            # update position
            self.piece_rect.topleft = square_to_position(self.square)

            return False
        else:
            # check if castling
            # if castling, move rook
            # king will be moved by code below castling check
            if board_state.engine_state.is_castling(
                grid_pos_to_move(self.grid_pos, new_grid_pos)
            ):
                self.handle_castling(new_grid_pos, board_state)

            # show piece animation
            if animate:
                self.animate_piece(
                    self.grid_pos, new_grid_pos, self.window_surface, self.piece_image
                )

            # update grid position
            self.grid_pos = new_grid_pos

            # update chess engine square
            self.square = grid_position_to_square(self.grid_pos)

            # update position
            self.piece_rect.topleft = square_to_position(self.square)

            return True

    import pygame

    def animate_piece(
        self,
        start_pos: GridPosition,
        end_pos: GridPosition,
        surface: pygame.surface.Surface,
        piece_image: pygame.surface.Surface,
    ):
        """
        Animate piece movement
        """
        start_square = grid_position_to_square(start_pos)
        end_square = grid_position_to_square(end_pos)

        start_x, start_y = square_to_position(start_square)
        end_x, end_y = square_to_position(end_square)

        clock = pygame.time.Clock()
        frames = 5  # number of frames in animation
        for i in range(frames):
            # calculate current x and y position of piece
            current_x = start_x + (end_x - start_x) * i / frames
            current_y = start_y + (end_y - start_y) * i / frames

            # blit piece onto surface
            surface.blit(piece_image, (current_x, current_y))

            # control animation speed
            clock.tick(60)

            # update display
            pygame.display.update()

    def handle_castling(self, new_grid_pos: GridPosition, board_state: BoardState):
        """
        Handle castling
        """
        rook_piece = self.is_castling(self.grid_pos, new_grid_pos, board_state)

        if rook_piece:
            rook_pos_new = self.get_rook_new_pos_after_castling(
                rook_piece, self.grid_pos, new_grid_pos, board_state
            )

            # update rook position
            rook_piece.grid_pos = rook_pos_new
            rook_piece.square = grid_position_to_square(rook_pos_new)
            rook_piece.piece_rect.topleft = square_to_position(rook_piece.square)

    def render(self) -> None:
        self.window_surface.blit(self.piece_image, self.piece_rect)

    def is_castling(
        self, oldpos: GridPosition, newpos: GridPosition, board_state: BoardState
    ) -> Any:
        """
        Check if castling is happening
        """
        # only kings can castle
        if self.piece_type != PieceType.King:
            return None

        if board_state.engine_state.is_kingside_castling(
            grid_pos_to_move(oldpos, newpos)
        ):
            if self.piece_colour == PieceColour.White:
                return self.get_piece_from_square(board_state, chess.H1)
            else:
                return self.get_piece_from_square(board_state, chess.H8)

        if board_state.engine_state.is_queenside_castling(
            grid_pos_to_move(oldpos, newpos)
        ):
            if self.piece_colour == PieceColour.White:
                return self.get_piece_from_square(board_state, chess.A1)
            else:
                return self.get_piece_from_square(board_state, chess.A8)

        return None

    def get_piece_from_square(self, board_state: BoardState, square: int) -> Any:
        """
        Get piece from square
        """
        for piece in board_state.pieces:
            if piece.square == square:
                return piece

        return None

    def get_rook_new_pos_after_castling(
        self,
        rook_piece: "Piece",
        oldpos: GridPosition,
        newpos: GridPosition,
        board_state: BoardState,
    ) -> GridPosition:
        """
        Get the new position of the rook after castling
        """
        if rook_piece is None:
            return GridPosition(-1, -1)

        if board_state.engine_state.is_kingside_castling(
            grid_pos_to_move(oldpos, newpos)
        ):
            return GridPosition(oldpos.row, oldpos.col + 1)

        if board_state.engine_state.is_queenside_castling(
            grid_pos_to_move(oldpos, newpos)
        ):
            return GridPosition(oldpos.row, oldpos.col - 1)

        return GridPosition(-1, -1)
