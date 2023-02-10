import chess
from typing import Optional, List, Tuple
from knightfight.types import GridPosition, PieceType, PieceColour
from helpers.log import LOGGER
from helpers import conversions

# add move to board state
def add_move_to_engine_state(
    engine_state: chess.Board,
    start: Optional[GridPosition | None],
    end: Optional[GridPosition | None],
    pt: PieceType,
) -> chess.Board:
    """
    Add a move to the board state
    """
    if start is None or end is None:
        return engine_state

    move = conversions.grid_pos_to_move(start, end)
    # move.drop = piece_type_to_piece(pt)
    engine_state.push(move)

    # Return the engine state
    LOGGER.debug(f"FEN: {engine_state.fen()}")
    return engine_state
