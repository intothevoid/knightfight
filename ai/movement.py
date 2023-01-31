"""
Control and verify movement of pieces on the board
"""

from chess.types import GridPosition, PieceType


# function that accepts GridPosition for start position and end position
# check if move is valid by chess piece type
# return True if valid, False if invalid

def is_move_valid(old_pos: GridPosition,
                  new_pos: GridPosition,
                  piece_type: PieceType) -> bool:
    if piece_type == PieceType.Pawn:
        return check_pawn_move(old_pos, new_pos)


# check if pawn move is valid
def check_pawn_move(old_pos: GridPosition, new_pos: GridPosition) -> bool:
    return True
