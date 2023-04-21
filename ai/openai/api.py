import re
import openai
import chess
from helpers.log import LOGGER
from typing import Optional

"""
Keep in mind that while this prompt provides clearer instructions, 
GPT models are not specialized for chess analysis. Therefore, you might 
still encounter some inaccuracies in the results. For optimal performance, 
consider using a dedicated chess engine like Stockfish.
"""


class OpenAIAPIWrapper:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def _generate_text(
        self,
        prompt,
        engine="text-davinci-002",
        max_tokens=150,
        n=1,
        stop=None,
        temperature=1.0,
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

    def get_next_chess_move(self, old_fen, color: chess.Color) -> Optional[chess.Move]:
        """
        Given a chess position in FEN notation, return the next chess move.
        """
        prompt = ""
        colorstr = ""
        if color == chess.WHITE:
            colorstr = "white"
        else:
            colorstr = "black"

        prompt += (
            f"Given the chess board position in FEN notation: {old_fen}, "
            f"what is the next best legal move for the {colorstr} player? "
            "Consider the existing positions of all pieces. Please provide "
            "the move in Universal Chess Interface (UCI) format. It is very important "
            "your response is a valid UCI move and has a minimum length of 4 characters."
        )

        # convert uci string to chess.Move
        resp = self._generate_text(prompt)

        resp_uci = ""
        # sometimes OpenAI responds as a sentence instead of a UCI move string
        if len(resp) > 5:
            resp_uci = self.extract_move_from_response(resp)
        else:
            resp_uci = resp

        if resp_uci and len(resp_uci) < 5:
            return chess.Move.from_uci(resp_uci)

        return None

    def extract_move_from_response(self, input_str):
        pattern = re.compile(r"\b[a-h][1-8][a-h]?[1-8]?\b")
        match = pattern.search(input_str)
        return match.group(0) if match else ""
