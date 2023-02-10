"""
Control and verify movement of pieces on the board
"""

from typing import List
import chess

from knightfight.types import GridPosition, PieceType, PieceColour
from helpers import conversions
from helpers.log import LOGGER


def validate_move(board: chess.Board, old_pos: GridPosition, new_pos: GridPosition):
    old_square = conversions.grid_position_to_square(old_pos)
    new_square = conversions.grid_position_to_square(new_pos)

    from_label = conversions.grid_position_to_label(old_pos)
    to_label = conversions.grid_position_to_label(new_pos)

    # check if the move is valid
    move = chess.Move(old_square, new_square)

    if move in board.legal_moves:
        return True
    else:
        LOGGER.info(f"Invalid move {from_label} -> {to_label} Result:{board.result()}")
    return False


def is_move_valid(
    old_pos: GridPosition,
    new_pos: GridPosition,
    engine_state: chess.Board,
) -> bool:
    """
    This function checks if piece moves are valid based on params like
    old position, new position, piece type and piece colour
    """

    if old_pos == new_pos:
        return False

    if old_pos.row < 0 or old_pos.row > 7:
        return False

    if old_pos.col < 0 or old_pos.col > 7:
        return False

    if new_pos.row < 0 or new_pos.row > 7:
        return False

    if new_pos.col < 0 or new_pos.col > 7:
        return False

    # check if old_pos to new_pos is a valid move
    return validate_move(engine_state, old_pos, new_pos)


def validate_path(
    piece_path: List[GridPosition],
    old_pos: GridPosition,
    new_pos: GridPosition,
    engine_state: chess.Board,
) -> bool:
    """
    This function checks if the new position is a valid move
    """
    if new_pos in piece_path:
        for pos in piece_path:
            # check if the path is blocked by any other piece
            if pos not in [old_pos, new_pos]:
                if is_position_occupied(pos, engine_state):
                    return False
        return True
    return False


def is_position_occupied(pos: GridPosition, engine_state: chess.Board) -> bool:
    """
    This function checks if the position is occupied by a piece
    """
    return conversions.is_position_occupied(engine_state, pos)
