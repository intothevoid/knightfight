import openai
import chess
from helpers.log import LOGGER


class OpenAIAPIWrapper:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def _generate_text(
        self,
        prompt,
        engine="text-davinci-002",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    ):
        """
        Generate text using OpenAI.
        """
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=max_tokens,
            n=n,
            stop=stop,
            temperature=temperature,
        )

        LOGGER.info(f"OpenAPI Response: {response.choices[0].text.strip()}")  # type: ignore

        return response.choices[0].text.strip()  # type: ignore

    def get_next_chess_move(self, old_fen):
        """
        Given a chess position in FEN notation, return the next chess move.
        """
        prompt = f"Given the chess position in FEN notation: {old_fen}, what is the best move? Please provide the resulting FEN representation after the move."
        new_fen = self._generate_text(prompt)

        # Check if the move is legal
        board = chess.Board(old_fen)
        legal_moves = list(board.legal_moves)

        for move in legal_moves:
            temp_board = board.copy()
            temp_board.push(move)
            if temp_board.fen() == new_fen:
                return move

        return None
