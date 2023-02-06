"""
Converts board positions of format (row, col) to readable format (a1, b2, etc.)
"""

from knightfight.types import GridPosition


def convert_grid_pos_to_algebraic_notation(pos: GridPosition) -> str:
    """
    Convert a grid position to a readable format
    """
    row = pos.row + 1
    col = pos.col + 1
    col = convert_col_to_algebraic(col)
    return f"{col}{row}"


def convert_col_to_algebraic(col: int) -> str:
    """
    Convert a column number to a readable format
    """
    if col == 1:
        return "a"
    elif col == 2:
        return "b"
    elif col == 3:
        return "c"
    elif col == 4:
        return "d"
    elif col == 5:
        return "e"
    elif col == 6:
        return "f"
    elif col == 7:
        return "g"
    elif col == 8:
        return "h"
    else:
        return "a"


def convert_algebraic_notation_to_grid_pos(pos: str) -> GridPosition:
    """
    Convert a readable position to a grid position
    """
    row = int(pos[1]) - 1
    col = convert_algebraic_to_col(pos[0])
    return GridPosition(row, col)


def convert_algebraic_to_col(col: str) -> int:
    """
    Convert a readable column to a column number
    """
    if col == "a":
        return 0
    elif col == "b":
        return 1
    elif col == "c":
        return 2
    elif col == "d":
        return 3
    elif col == "e":
        return 4
    elif col == "f":
        return 5
    elif col == "g":
        return 6
    elif col == "h":
        return 7
    else:
        return 0
