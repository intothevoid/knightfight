"""
Move related functionality using python chess
"""

from typing import Optional, Tuple
import chess
from ai.lookup import CHESS_SQUARE_TO_POS
from knightfight.types import GridPosition, PieceColour, PieceType
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


def grid_pos_to_square(grid_pos: GridPosition) -> chess.Square:
    """
    Convert a grid position to a chess square
    """
    return chess.square(grid_pos.col, grid_pos.row)


# flipped version of the above
def grid_pos_to_move(start_pos: GridPosition, end_pos: GridPosition) -> chess.Move:
    """
    Convert a start and end grid position to a chess move
    """
    # flip start_pos vertically as our internal representation is flipped
    start_pos = GridPosition(start_pos.row, start_pos.col)

    # flip end_pos vertically as our internal representation is flipped
    end_pos = GridPosition(end_pos.row, end_pos.col)

    return chess.Move(grid_pos_to_square(start_pos), grid_pos_to_square(end_pos))


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

    move = grid_pos_to_move(start, end)
    # move.drop = piece_type_to_piece(pt)
    engine_state.push(move)

    # Return the engine state
    LOGGER.debug(f"FEN: {engine_state.fen()}")
    return engine_state


def is_king_in_check(engine_state: chess.Board, color: PieceColour) -> bool:
    """
    Check if the king of the given color is in check
    """
    if color == PieceColour.White:
        return engine_state.is_check()
    return engine_state.is_checkmate()


def piece_type_to_piece(piece_type: PieceType) -> chess.PieceType:
    """
    Convert an internal PieceType to a chess.Piece
    """
    return chess.Piece.from_symbol(FEN_CONVERSION[piece_type].upper()).piece_type


def square_to_position(square: int) -> Tuple[int, int]:
    """
    Convert a chess square to a position
    """
    if square in CHESS_SQUARE_TO_POS:
        return CHESS_SQUARE_TO_POS[square]
    return (0, 0)


def position_to_square(position: Tuple[int, int]) -> int:
    """
    Convert a position to a chess square
    """
    for square in CHESS_SQUARE_TO_POS:
        if CHESS_SQUARE_TO_POS[square] == position:
            return square
    return 0


def position_to_grid_position(position: Tuple[int, int]) -> GridPosition:
    """
    Convert a position to a grid position
    """
    row = (position[0] - 40) // 90
    col = (position[1] - 40) // 90
    return GridPosition(row, col)


def grid_position_to_position(grid_position: GridPosition) -> Tuple[int, int]:
    """
    Convert a grid position to a position
    """
    row = grid_position.row
    col = grid_position.col
    return (40 + row * 90, 40 + col * 90)


def square_to_grid_position(square: int) -> GridPosition:
    """
    Convert a chess square to a grid position
    """
    row, col = divmod(square, 8)
    return GridPosition(row, col)


def grid_position_to_square(grid_position: GridPosition) -> int:
    """
    Convert a grid position to a chess square
    """
    return chess.square(grid_position.col, grid_position.row)


def is_position_occupied(
    engine_state: chess.Board, grid_position: GridPosition
) -> bool:
    """
    Check if a position is occupied on the board
    """
    return engine_state.piece_at(grid_position_to_square(grid_position)) is not None
