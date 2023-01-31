"""
Control and verify movement of pieces on the board
"""

from chess.types import GridPosition, PieceType, PieceColour


def is_move_valid(
    old_pos: GridPosition,
    new_pos: GridPosition,
    piece_type: PieceType,
    piece_color: PieceColour,
) -> bool:
    """
    This function checks if piece moves are valid based on params like
    old position, new position, piece type and piece colour
    """

    if piece_type == PieceType.Pawn:
        return check_pawn_move(old_pos, new_pos, piece_color)
    if piece_type == PieceType.Knight:
        return check_knight_move(old_pos, new_pos)
    if piece_type == PieceType.Rook:
        return check_rook_move(old_pos, new_pos)
    if piece_type == PieceType.Bishop:
        return check_bishop_move(old_pos, new_pos)
    if piece_type == PieceType.Queen:
        return check_queen_move(old_pos, new_pos)
    if piece_type == PieceType.King:
        return check_king_move(old_pos, new_pos)


def check_pawn_move(
    old_pos: GridPosition, new_pos: GridPosition, piece_color: PieceColour
) -> bool:
    """
    Check if pawn move is valid

    """
    row_diff = abs(old_pos.row - new_pos.row)
    col_diff = abs(old_pos.col - new_pos.col)

    if piece_color == PieceColour.White:
        # white pawns move up the board
        if new_pos.row > old_pos.row:
            return False
        if row_diff == 2 and col_diff == 0 and old_pos.row == 6:
            return True
        if row_diff == 1 and col_diff == 0:
            return True
    else:
        # black pawns move down the board
        if new_pos.row < old_pos.row:
            return False
        if row_diff == 2 and col_diff == 0 and old_pos.row == 1:
            return True
        if row_diff == 1 and col_diff == 0:
            return True

    return False


def check_knight_move(old_pos: GridPosition, new_pos: GridPosition) -> bool:
    """
    Check if a knight move is valid
    """
    row_diff = abs(new_pos.row - old_pos.row)
    col_diff = abs(new_pos.col - old_pos.col)

    if row_diff == 2 and col_diff == 1:
        return True
    elif row_diff == 1 and col_diff == 2:
        return True

    return False


def check_rook_move(old_pos: GridPosition, new_pos: GridPosition) -> bool:
    """
    Check if a rook move is valid
    """
    if old_pos.row == new_pos.row or old_pos.col == new_pos.col:
        return True
    else:
        return False


def check_bishop_move(old_pos: GridPosition, new_pos: GridPosition) -> bool:
    """
    Check if a bishop move is valid
    """
    row_diff = abs(new_pos.row - old_pos.row)
    col_diff = abs(new_pos.col - old_pos.col)

    if row_diff == col_diff:
        return True
    else:
        return False


def check_king_move(old_pos: GridPosition, new_pos: GridPosition) -> bool:
    """
    Check if a king move is valid
    """
    row_diff = abs(new_pos.row - old_pos.row)
    col_diff = abs(new_pos.col - old_pos.col)

    if (
        row_diff <= 1
        and col_diff <= 1
        and (old_pos.row, old_pos.col) != (new_pos.row, new_pos.col)
    ):
        return True
    else:
        return False


def check_queen_move(old_pos: GridPosition, new_pos: GridPosition) -> bool:
    """
    Check if a queen move is valid
    """
    row_diff = abs(new_pos.row - old_pos.row)
    col_diff = abs(new_pos.col - old_pos.col)

    if row_diff == col_diff or row_diff == 0 or col_diff == 0:
        return True
    else:
        return False
