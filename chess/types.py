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
        self.row = None
        self.col = None
