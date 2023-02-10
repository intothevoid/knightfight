"""
Move related functionality using python chess
"""

from typing import Optional, Tuple
import chess
from ai.lookup import CHESS_SQUARE_TO_POS
from knightfight.types import GridPosition, PieceColour, PieceType
from knightfight.types import FEN_CONVERSION
from helpers.log import LOGGER


def grid_pos_to_square(grid_pos: GridPosition) -> chess.Square:
    """
    Convert a grid position to a chess square
    """
    return chess.square(grid_pos.col, grid_pos.row)


# flipped version of the above
def grid_pos_to_move(start_pos: GridPosition, end_pos: GridPosition) -> chess.Move:
    """
    Convert a start and end grid position to a chess move
    """
    return chess.Move(grid_pos_to_square(start_pos), grid_pos_to_square(end_pos))


def piece_type_to_piece(piece_type: PieceType) -> chess.PieceType:
    """
    Convert an internal PieceType to a chess.Piece
    """
    return chess.Piece.from_symbol(FEN_CONVERSION[piece_type].upper()).piece_type


def square_to_position(square: int) -> Tuple[int, int]:
    """
    Convert a chess square to a position
    """
    if square in CHESS_SQUARE_TO_POS:
        return CHESS_SQUARE_TO_POS[square]
    return (0, 0)


def position_to_square(position: Tuple[int, int]) -> int:
    """
    Convert a position to a chess square
    """
    for square in CHESS_SQUARE_TO_POS:
        if CHESS_SQUARE_TO_POS[square] == position:
            return square
    return 0


def position_to_grid_position(position: Tuple[int, int]) -> GridPosition:
    """
    Convert a position to a grid position
    """
    row = (position[0] - 40) // 90
    col = (position[1] - 40) // 90
    return GridPosition(row, col)


def grid_position_to_square(grid_position: GridPosition) -> int:
    """
    Convert a grid position to a chess square
    """
    return chess.square(grid_position.col, grid_position.row)


def is_position_occupied(
    engine_state: chess.Board, grid_position: GridPosition
) -> bool:
    """
    Check if a position is occupied on the board
    """
    return engine_state.piece_at(grid_position_to_square(grid_position)) is not None


# grid position to label
def grid_position_to_label(grid_position: GridPosition) -> str:
    """
    Convert a grid position to a label
    """
    collbl = ["a", "b", "c", "d", "e", "f", "g", "h"]
    return f"{collbl[grid_position.col]}{grid_position.row + 1}"
