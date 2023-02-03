from typing import List, Any  # use Any instead of Piece to avoid circular import
from chess.types import PieceColour, PieceType
from chess.types import GridPosition


class BoardState:
    def __init__(self) -> None:
        """
        Initialize the board state
        """
        self.board_state = {
            PieceColour.Black: {
                PieceType.Pawn: [],
                PieceType.Knight: [],
                PieceType.Rook: [],
                PieceType.Bishop: [],
                PieceType.Queen: [],
                PieceType.King: [],
            },
            PieceColour.White: {
                PieceType.Pawn: [],
                PieceType.Knight: [],
                PieceType.Rook: [],
                PieceType.Bishop: [],
                PieceType.Queen: [],
                PieceType.King: [],
            },
        }

        self._pieces = []
        self._killed_pieces = []
        self._changed_pieces = []

    @property
    def pieces(self) -> List[Any]:
        return self._pieces

    @pieces.setter
    def pieces(self, pieces: List[Any]) -> None:
        self._pieces = pieces

    @property
    def killed_pieces(self) -> List[Any]:
        return self._killed_pieces

    @killed_pieces.setter
    def killed_pieces(self, killed_pieces: List[Any]) -> None:
        self._killed_pieces = killed_pieces

    @property
    def changed_pieces(self) -> List[Any]:
        return self._changed_pieces

    @changed_pieces.setter
    def changed_pieces(self, changed_pieces: List[Any]) -> None:
        self._changed_pieces = changed_pieces

    def update_board_state(
        self,
    ) -> None:
        """
        Set the board state based on the pieces on the board
        """
        for piece in self._pieces:
            self.board_state[piece.piece_colour][piece.piece_type].append(
                piece.grid_pos
            )

    def get_board_state(self) -> dict:
        """
        Get the board state
        """
        return self.board_state

    def get_starting_positions(self) -> dict:
        """
        Initial board positions
        """
        starting_positions = {
            PieceType.Pawn: [
                (1, 0),
                (1, 1),
                (1, 2),
                (1, 3),
                (1, 4),
                (1, 5),
                (1, 6),
                (1, 7),
                (6, 0),
                (6, 1),
                (6, 2),
                (6, 3),
                (6, 4),
                (6, 5),
                (6, 6),
                (6, 7),
            ],
            PieceType.Knight: [(0, 1), (0, 6), (7, 1), (7, 6)],
            PieceType.Rook: [(0, 0), (0, 7), (7, 0), (7, 7)],
            PieceType.Bishop: [(0, 2), (0, 5), (7, 2), (7, 5)],
            PieceType.Queen: [(0, 3), (7, 3)],
            PieceType.King: [(0, 4), (7, 4)],
        }

        return starting_positions