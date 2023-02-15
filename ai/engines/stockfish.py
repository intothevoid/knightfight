from typing import Optional
import chess
import chess.engine
from knightfight.types import Engine


class StockFishEngine(Engine):
    def __init__(self, engine_path: str) -> None:
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)

    def get_informed_move(self, board: chess.Board) -> Optional[chess.Move]:
        # Get the move
        result = self.engine.play(board, chess.engine.Limit(time=0.1))

        # Return the move
        if result:
            return result.move
        return None

    def quit(self) -> None:
        self.engine.quit()
