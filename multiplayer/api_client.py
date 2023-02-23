"""
Functions to make get, post, put and delete requests to the API
"""

import requests
from typing import List, Optional
from multiplayer.models import (
    GamesGetResponse,
    GamesPostRequest,
    GamesPostResponse,
    GamesGameIdGetResponse,
    GamesGameIdPutRequest,
    GamesGameIdPutResponse,
    GamesGameIdDeleteResponse,
)

from config.config import APP_CONFIG

CHESSAPI_SERVER = APP_CONFIG["multiplayer"]["server"] or "http://localhost:8000"
API_URL = f"{CHESSAPI_SERVER}/api/v1"


def get_games_request() -> List[GamesGetResponse]:
    """
    Get all games from the API
    """
    games = []
    response = requests.get(f"{API_URL}/games")
    if response.status_code == 200:
        for game in response.json():
            games.append(GamesGetResponse(**game))
    return games


def get_game_request(game_id: str) -> Optional[GamesGameIdGetResponse]:
    """
    Get a game from the API
    """
    response = requests.get(f"{API_URL}/games/{game_id}")
    if response.status_code == 200:
        return GamesGameIdGetResponse(**response.json())
    return None


def create_game_request(game: GamesPostRequest) -> Optional[GamesPostResponse]:
    """
    Create a game in the API
    """
    response = requests.post(f"{API_URL}/games", json=game.dict())
    if response.status_code == 201:
        return GamesPostResponse(**response.json())
    return None


def update_game_request(
    game_id: str, game: GamesGameIdPutRequest
) -> Optional[GamesGameIdPutResponse]:
    """
    Update a game in the API
    """
    response = requests.put(
        f"{API_URL}/games/{game_id}", json=game.dict(exclude_unset=True)
    )
    if response.status_code == 200:
        return GamesGameIdPutResponse(**response.json())
    return None


def delete_game_request(game_id: str) -> Optional[GamesGameIdDeleteResponse]:
    """
    Delete a game from the API
    """
    response = requests.delete(f"{API_URL}/games/{game_id}")
    if response.status_code == 204:
        return GamesGameIdDeleteResponse(id=game_id)
    return None
