import chess
from typing import List, Any
from ai.engine import (
    state_to_engine_state,
)
from knightfight.types import PieceColour, PieceType, State


class BoardState(State):
    def __init__(self) -> None:
        """
        Initialize the board state
        """
        # board state
        self.board_state = self.get_cleared_state()

        # pieces on the board
        self._pieces = []
        self._killed_pieces = []
        self._changed_pieces = []
        self._dragged_piece = None

        # game state
        self.game_over = False
        self.winner = None

        # engine state
        self._engine_state = chess.Board()

    def get_cleared_state(self) -> dict:
        """
        Get a cleared board state
        """
        return {
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

    @property
    def dragged_piece(self) -> Any:
        return self._dragged_piece

    @dragged_piece.setter
    def dragged_piece(self, dragged_piece: Any) -> None:
        self._dragged_piece = dragged_piece

    @property
    def engine_state(self) -> chess.Board:
        """
        Get the engine state
        Convert the board state to the engine state before returning
        """
        self.engine_state = state_to_engine_state(self.board_state)
        return self._engine_state

    @engine_state.setter
    def engine_state(self, engine_state: chess.Board) -> None:
        self._engine_state = engine_state

    def update_board_state(
        self,
    ) -> None:
        """
        Set the board state based on the pieces on the board
        """
        self.board_state.clear()
        self.board_state = self.get_cleared_state()

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
