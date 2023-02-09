from helpers.log import LOGGER
import chess


class AIPlayer:
    def __init__(self, color: chess.Color):
        self.color = color

    def move(self, board: chess.Board):
        legal_moves = list(board.legal_moves)
        move = legal_moves[0] if legal_moves else None

        # update board with move
        if move:
            # get piece
            piece = board.piece_at(move.from_square)

            board.push(move)

            if len(board.move_stack) > 0 and piece:
                LOGGER.info(
                    f"Moved {piece.color} {piece.piece_type} {board.move_stack[-1]}"
                )
        else:
            LOGGER.info("No legal moves. Game over.")
