import chess
from helpers.log import LOGGER
from sound.playback import play_sound
from multiplayer.api_client import (
    create_game_request,
    delete_game_request,
    get_game_request,
    update_game_request,
)

from multiplayer.models import (
    GamesPostRequest,
    GamesGameIdPutRequest,
)


class NetworkPlayer:
    def __init__(
        self,
        color: chess.Color,
        name: str = "NetworkPlayer",
    ):
        self.color = color
        self.name = name
        self.other_player = ""
        self.game_id = ""
        self.board = chess.Board()

    def create_game(self) -> bool:
        """
        Create a game on the server
        """
        create_request = GamesPostRequest(
            player1=self.name,
            player2="",
            state=self.board.fen(),
        )

        # create a game on the server
        resp = create_game_request(create_request)

        # get the id of the game created
        if resp:
            self.game_id = resp.id

            # get game state from server
            if self.game_id:
                game_data_resp = get_game_request(self.game_id)
                if game_data_resp:
                    self.state = game_data_resp.state
                    if self.name == game_data_resp.player1:
                        self.other_player = game_data_resp.player2
                    else:
                        self.other_player = game_data_resp.player1

                    return True

        return False

    def record_self_move_to_server(self, move: chess.Move) -> bool:
        """
        Once the player has made a move, record it to the server
        """

        # record the move to the server
        update_request = GamesGameIdPutRequest(
            state=self.board.fen(),
        )

        if self.game_id:
            resp = update_game_request(self.game_id, update_request)
            if resp and resp.id:
                return True

        return False

    def get_other_player_move_from_server(self) -> bool:
        """
        Get the other player's move from the server
        """
        if self.game_id:
            game_data_resp = get_game_request(self.game_id)
            if game_data_resp:
                if self.board.fen() != game_data_resp.state:
                    self.board = chess.Board(game_data_resp.state)
                    return True
        return False

    def delete_game(self) -> bool:
        """
        Delete the game from the server
        """
        if self.game_id:
            resp = delete_game_request(self.game_id)
            if resp:
                return True
        return False
