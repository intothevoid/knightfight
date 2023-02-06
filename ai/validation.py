"""
Control and verify movement of pieces on the board
"""

from typing import List
from knightfight.types import GridPosition, PieceType, PieceColour, State
from ai.paths import (
    get_bishop_path,
    get_king_path,
    get_knight_path,
    get_pawn_path,
    get_queen_path,
    get_rook_path,
)


def is_move_valid(
    old_pos: GridPosition,
    new_pos: GridPosition,
    piece_type: PieceType,
    piece_colour: PieceColour,
    board_state: State,
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

    if piece_type == PieceType.Pawn:
        # check if end position is occupied
        # cannot kill piece by moving forward, must move diagonally
        end_pos_occupied = True if is_position_occupied(new_pos, board_state) else False
        piece_path = get_pawn_path(old_pos, new_pos, piece_colour, end_pos_occupied)
        return validate_path(piece_path, old_pos, new_pos, board_state)
    if piece_type == PieceType.Knight:
        # for knight piece, we can jump over other pieces
        piece_path = get_knight_path(old_pos, new_pos)
        return validate_path(piece_path, old_pos, new_pos, board_state)
    if piece_type == PieceType.Rook:
        piece_path = get_rook_path(old_pos, new_pos)
        return validate_path(piece_path, old_pos, new_pos, board_state)
    if piece_type == PieceType.Bishop:
        piece_path = get_bishop_path(old_pos, new_pos)
        return validate_path(piece_path, old_pos, new_pos, board_state)
    if piece_type == PieceType.Queen:
        piece_path = get_queen_path(old_pos, new_pos)
        return validate_path(piece_path, old_pos, new_pos, board_state)
    if piece_type == PieceType.King:
        piece_path = get_king_path(old_pos, new_pos)
        return validate_path(piece_path, old_pos, new_pos, board_state)

    # invalid piece type passed
    return False


def validate_path(
    piece_path: List[GridPosition],
    old_pos: GridPosition,
    new_pos: GridPosition,
    board_state: State,
) -> bool:
    """
    This function checks if the new position is a valid move
    """
    if new_pos in piece_path:
        for pos in piece_path:
            # check if the path is blocked by any other piece
            if pos not in [old_pos, new_pos]:
                if is_position_occupied(pos, board_state):
                    return False
        return True
    return False


def is_position_occupied(pos: GridPosition, board_state: State) -> bool:
    """
    This function checks if the position is occupied by a piece
    """
    state = board_state.get_board_state()
    black_pieces = state[PieceColour.Black]
    white_pieces = state[PieceColour.White]

    for _, pieces in black_pieces.items():
        for piece in pieces:
            if piece == pos:
                return True

    for _, pieces in white_pieces.items():
        for piece in pieces:
            if piece == pos:
                return True

    return False
