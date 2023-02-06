from dataclasses import dataclass
from enum import Enum
import abc

# enum for the piece types
class PieceType(Enum):
    Bishop = "Bishop"
    King = "King"
    Knight = "Knight"
    Pawn = "Pawn"
    Queen = "Queen"
    Rook = "Rook"
    Empty = "Empty"


# enum for the piece colours
class PieceColour(Enum):
    Black = "B"
    White = "W"
    Empty = "Empty"


FEN_CONVERSION = {
    PieceType.Pawn: "p",
    PieceType.Knight: "n",
    PieceType.Rook: "r",
    PieceType.Bishop: "b",
    PieceType.Queen: "q",
    PieceType.King: "k",
}


@dataclass
class GridPosition:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self) -> str:
        return f"GridPosition row:{self.row} col:{self.col}"

    def __eq__(self, other) -> bool:
        """
        Compare two GridPosition objects
        """
        if isinstance(other, GridPosition):
            return self.row == other.row and self.col == other.col
        return False


class State(abc.ABC):
    """
    Abstract class for the board state
    """

    @abc.abstractmethod
    def get_cleared_state(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def update_board_state(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_board_state(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def get_starting_positions(self) -> dict:
        raise NotImplementedError
