from dataclasses import dataclass

# enum for the piece types


class PieceType:
    Bishop = "Bishop"
    King = "King"
    Knight = "Knight"
    Pawn = "Pawn"
    Queen = "Queen"
    Rook = "Rook"
    Empty = "Empty"


# enum for the piece colours
class PieceColour:
    Black = "B"
    White = "W"
    Empty = "Empty"


@dataclass
class GridPosition:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self) -> str:
        return f"GridPosition row:{self.row} col:{self.col}"
