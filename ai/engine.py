"""
Move related functionality using python chess
"""

import chess
from knightfight.types import PieceColour
from knightfight.types import FEN_CONVERSION
from helpers.log import LOGGER


def state_to_engine_state(state_dict: dict) -> chess.Board:
    """
    Convert the board state (our internal represenation) to the engine state (FEN)
    """
    # Create a chess board
    board = chess.Board()

    # Set all pieces on the board
    for color in state_dict:
        for piece_type in state_dict[color]:
            for grid_pos in state_dict[color][piece_type]:
                row, col = grid_pos.row, grid_pos.col
                piece = chess.Piece.from_symbol(
                    FEN_CONVERSION[piece_type].upper()
                    if color == PieceColour.White
                    else FEN_CONVERSION[piece_type].lower()
                )
                board.set_piece_at(chess.square(col, row), piece)

    # IMPORTANT!
    # flip board as our interal representation is flipped
    # compared to the engine state. python lists start at 0
    board = board.transform(chess.flip_vertical)

    # Return the engine state
    LOGGER.debug(f"FEN: {board.fen()}")
    return board


def is_king_in_check(engine_state: chess.Board, color: PieceColour) -> bool:
    """
    Check if the king of the given color is in check
    """
    if color == PieceColour.White:
        return engine_state.is_check()
    return engine_state.is_checkmate()
