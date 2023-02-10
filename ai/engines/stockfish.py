from typing import Optional
import chess
import chess.engine


def get_informed_move(board: chess.Board) -> Optional[chess.Move]:
    engine = chess.engine.SimpleEngine.popen_uci(r"assets/engines/stockfish")

    # Get the move
    result = engine.play(board, chess.engine.Limit(time=0.1))

    # Close the engine
    engine.quit()

    # Return the move
    if result:
        return result.move
    return None
