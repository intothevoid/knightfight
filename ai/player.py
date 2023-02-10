import random
import chess
from ai.lookup import CHESS_SQUARE_TO_POS
from config.config import APP_CONFIG
from helpers.log import LOGGER
from knightfight.board import Board
from sound.playback import play_sound
from ai.piece_squares import selectmove


class AIPlayer:
    def __init__(
        self,
        color: chess.Color,
        sound_vol: float = 1.0,
        ai: str = "basic",
        complexity: int = 1,
    ):
        self.color = color
        self.sound_vol = sound_vol
        self.original_pos = None
        self.new_pos = None
        self.ai = ai
        self.complexity = complexity

    def move(self, board: Board) -> bool:
        legal_moves = list(board.state.engine_state.legal_moves)
        if len(legal_moves) > 0:
            if self.ai == "piece_squares":
                move = selectmove(board.state.engine_state, self.complexity)
            else:
                move = random.choice(legal_moves)

            # update board with move
            if move and move in legal_moves:
                # get piece
                to_square = move.to_square
                from_square = move.from_square

                # get piece
                board.state.engine_state.piece_at(move.from_square)
                moved_piece = None
                for piece in board.state.pieces:
                    if piece.square == from_square:
                        moved_piece = piece

                new_pos = CHESS_SQUARE_TO_POS[to_square]
                if moved_piece:
                    # move piece and update position
                    self.original_pos = moved_piece.grid_pos
                    piece_moved = board.move_piece(moved_piece, new_pos)
                    self.new_pos = moved_piece.grid_pos

                    if piece_moved:
                        play_sound("drop.mp3", self.sound_vol)
                    else:
                        play_sound("invalid_move.mp3", self.sound_vol)
                else:
                    LOGGER.error(f"Piece not found at square {from_square}")

                return True
            else:
                LOGGER.error("No legal moves found. This should not happen. Game Over?")
                return False
        else:
            LOGGER.info("No legal moves found. This should not happen. Game Over?")
            return False
