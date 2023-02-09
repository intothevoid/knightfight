import chess
from typing import List, Any
from knightfight.types import PieceColour, PieceType, State


class BoardState(State):
    def __init__(self) -> None:
        """
        Initialize the board state
        """
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
        return self._engine_state

    @engine_state.setter
    def engine_state(self, engine_state: chess.Board) -> None:
        self._engine_state = engine_state

    def get_board_state(self) -> chess.Board:
        return self._engine_state
