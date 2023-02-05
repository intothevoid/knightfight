"""
Control and verify movement of pieces on the board
"""

from chess.types import GridPosition, PieceType, PieceColour
from chess.state import BoardState
from typing import List


def is_move_valid(
    old_pos: GridPosition,
    new_pos: GridPosition,
    piece_type: PieceType,
    piece_colour: PieceColour,
    board_state: BoardState,
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
        piece_path = get_pawn_path(old_pos, new_pos, piece_colour, board_state)
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
    board_state: BoardState,
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


def is_position_occupied(pos: GridPosition, board_state: BoardState) -> bool:
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


def get_pawn_path(
    start: GridPosition, end: GridPosition, color: PieceColour, board_state: BoardState
) -> List[GridPosition]:
    start_row, start_col = start.row, start.col
    end_row, end_col = end.row, end.col
    path = []

    if color == PieceColour.White:
        # check if the move is along the column
        if start_col == end_col:
            # check if move is valid
            if (start_row - end_row) in [1, 2]:
                # check if pawn is moving two squares and is in starting position
                if (start_row - end_row) == 2 and start_row != 6:
                    return []

                # check if pawn is moving in the right direction
                if end_row > start_row:
                    return []

                # check if end position is occupied
                # cannot kill piece by moving forward, must move diagonally
                if is_position_occupied(end, board_state):
                    return []

                for row in range(start_row, end_row, -1):
                    path.append(GridPosition(row, start_col))
                path.append(end)
        else:
            # check if the move is diagonal
            if (start_row - end_row) == 1 and abs(start_col - end_col) == 1:
                # pawn is about to kill a piece diagonally
                # cannot move diagonally if the position is empty
                if is_position_occupied(end, board_state):
                    path.append(end)

    if color == PieceColour.Black:
        # check if the move is along the column
        if start_col == end_col:
            # check if move is valid
            if (end_row - start_row) in [1, 2]:
                # check if pawn is moving two squares and is in starting position
                if (end_row - start_row) == 2 and start_row != 1:
                    return []

                # check if pawn is moving in the right direction
                if end_row < start_row:
                    return []

                # check if end position is occupied
                # cannot kill piece by moving forward, must move diagonally
                if is_position_occupied(end, board_state):
                    return []

                for row in range(start_row, end_row):
                    path.append(GridPosition(row, start_col))
                path.append(end)
        else:
            # check if the move is diagonal
            if (end_row - start_row) == 1 and abs(start_col - end_col) == 1:
                # pawn is about to kill a piece diagonally
                # cannot move diagonally if the position is empty
                if is_position_occupied(end, board_state):
                    path.append(end)

    return path


def get_rook_path(start: GridPosition, end: GridPosition) -> List[GridPosition]:
    start_row, start_col = start.row, start.col
    end_row, end_col = end.row, end.col
    path = []

    # check if move is along the row
    if start_row == end_row:
        for col in range(min(start_col, end_col), max(start_col, end_col) + 1):
            path.append(GridPosition(start_row, col))
    # check if move is along the column
    elif start_col == end_col:
        for row in range(min(start_row, end_row), max(start_row, end_row) + 1):
            path.append(GridPosition(row, start_col))
    return path


def get_knight_path(start: GridPosition, end: GridPosition) -> List[GridPosition]:
    start_row, start_col = start.row, start.col
    end_row, end_col = end.row, end.col
    path = []

    # check if move is valid
    if abs(start_row - end_row) in [1, 2] and abs(start_col - end_col) in [1, 2]:
        if abs(start_row - end_row) != abs(start_col - end_col):
            path.append(end)

    return path


def get_bishop_path(start: GridPosition, end: GridPosition) -> List[GridPosition]:
    start_row, start_col = start.row, start.col
    end_row, end_col = end.row, end.col
    path = []

    # check if move is along a diagonal
    if abs(start_row - end_row) == abs(start_col - end_col):
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1
        path = []
        for row, col in zip(
            range(start_row, end_row, row_step), range(start_col, end_col, col_step)
        ):
            path.append(GridPosition(row, col))

        # add the end position
        path.append(end)

    return path


def get_queen_path(start: GridPosition, end: GridPosition) -> List[GridPosition]:
    start_row, start_col = start.row, start.col
    end_row, end_col = end.row, end.col
    path = []

    # check if move is along row
    if start_row == end_row:
        # check if move is to the right or left
        if start_col < end_col:
            # move to the right
            path = [
                GridPosition(start_row, col) for col in range(start_col, end_col + 1)
            ]
        else:
            # move to the left
            path = [
                GridPosition(start_row, col) for col in range(end_col, start_col + 1)
            ]

    # check if move is along column
    elif start_col == end_col:
        # check if move is up or down
        if start_row < end_row:
            # move down
            path = [
                GridPosition(row, start_col) for row in range(start_row, end_row + 1)
            ]
        else:
            # move up
            path = [
                GridPosition(row, start_col) for row in range(end_row, start_row + 1)
            ]

    # check if move is along diagonal
    elif abs(start_row - end_row) == abs(start_col - end_col):
        # check if move is up-right, up-left, down-right, or down-left
        row_dir = 1 if end_row > start_row else -1
        col_dir = 1 if end_col > start_col else -1
        path = []
        row, col = start_row, start_col
        while row != end_row and col != end_col:
            row += row_dir
            col += col_dir
            path.append(GridPosition(row, col))

    return path


def get_king_path(start: GridPosition, end: GridPosition) -> List[GridPosition]:
    start_row, start_col = start.row, start.col
    end_row, end_col = end.row, end.col
    path = []

    # check if the move is one square in any direction (horizontally, vertically, or diagonally)
    if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
        path.append(start)
        path.append(end)

    return path
