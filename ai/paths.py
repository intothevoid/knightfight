from knightfight.types import GridPosition, PieceColour, State
from typing import List


def get_pawn_path(
    start: GridPosition, end: GridPosition, color: PieceColour, end_pos_occupied: bool
) -> List[GridPosition]:
    start_row, start_col = start.row, start.col
    end_row, end_col = end.row, end.col
    path = []

    if color == PieceColour.White:
        # check if the move is along the column
        if start_col == end_col:
            # check if move is valid
            if (start_row - end_row) in [1, 2]:
                # check if pawn is moving two squares and is not in starting position
                if (start_row - end_row) == 2 and start_row != 6:
                    return []

                # check if pawn is moving in the right direction
                # valid move is from 6 to 4, not 4 to 6
                if end_row > start_row:
                    return []

                # check if end position is occupied
                # cannot kill piece by moving forward, must move diagonally
                if end_pos_occupied:
                    return []

                for row in range(start_row, end_row, -1):
                    path.append(GridPosition(row, start_col))
                path.append(end)
        else:
            # check if the move is diagonal
            if (start_row - end_row) == 1 and abs(start_col - end_col) == 1:
                # pawn is about to kill a piece diagonally
                # cannot move diagonally if the position is empty
                if end_pos_occupied:
                    path.append(end)

    if color == PieceColour.Black:
        # check if the move is along the column
        if start_col == end_col:
            # check if move is valid
            if (end_row - start_row) in [1, 2]:
                # check if pawn is moving two squares and is not in starting position
                if (end_row - start_row) == 2 and start_row != 1:
                    return []

                # check if pawn is moving in the right direction
                # valid move is from 1 to 3, not 3 to 1
                if end_row < start_row:
                    return []

                # check if end position is occupied
                # cannot kill piece by moving forward, must move diagonally
                if end_pos_occupied:
                    return []

                for row in range(start_row, end_row):
                    path.append(GridPosition(row, start_col))
                path.append(end)
        else:
            # check if the move is diagonal
            if (end_row - start_row) == 1 and abs(start_col - end_col) == 1:
                # pawn is about to kill a piece diagonally
                # cannot move diagonally if the position is empty
                if end_pos_occupied:
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
