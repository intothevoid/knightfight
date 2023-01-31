"""
The board class to capture the state of the chess board.
"""

import pygame
from chess.piece import Piece
from config import config
from chess.types import PieceType, PieceColour
from chess.types import GridPosition
from ai.movement import is_move_valid


class Board:
    def __init__(self, window_surface: pygame.surface.Surface) -> None:
        board_size = config.APP_CONFIG["board"]["size"]
        board_image = config.APP_CONFIG["board"]["image"]

        self.window_surface = window_surface
        self.board_image = pygame.image.load(f"assets/{board_image}")
        self.board_rect = self.board_image.get_rect()
        self.board_rect.topleft = (0, 0)
        self.board_image = pygame.transform.scale(
            self.board_image, (board_size, board_size)
        )

        # maintain a list of pieces on the board
        self.pieces = []

        # initialize the pieces
        self.init_pieces()

    def init_pieces(self) -> None:
        # initialize the pieces
        starting_positions = {
            PieceType.Pawn: [
                (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
                (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7)
            ],
            PieceType.Knight: [
                (0, 1), (0, 6),
                (7, 1), (7, 6)
            ],
            PieceType.Rook: [
                (0, 0), (0, 7),
                (7, 0), (7, 7)
            ],
            PieceType.Bishop: [
                (0, 2), (0, 5),
                (7, 2), (7, 5)
            ],
            PieceType.Queen: [(0, 3), (7, 3)],
            PieceType.King: [(0, 4), (7, 4)],
        }

        for piece_type, positions in starting_positions.items():
            for row, col in positions:
                piece_colour = PieceColour.Black if row in [
                    0, 1] else PieceColour.White
                piece_pos = (40 + col * 90, 40 + row * 90)
                piece = Piece(self.window_surface, piece_type, piece_colour,
                              piece_pos, GridPosition(row, col))
                self.add_piece(piece)

    def add_piece(self, piece: Piece) -> None:
        self.pieces.append(piece)

    def remove_piece(self, piece: Piece) -> None:
        self.pieces.remove(piece)

    def get_piece(self, piece_pos) -> Piece:
        for piece in self.pieces:
            if piece.piece_pos == piece_pos:
                return piece

        return None

    def move_piece(self, piece: Piece, new_pos: GridPosition) -> None:
        old_pos = piece.grid_pos

        # check if move is valid
        if is_move_valid(old_pos, new_pos, piece.piece_type):
            piece.piece_pos = new_pos
            piece.piece_rect.topleft = new_pos
        else:
            # move is invalid
            # TODO
            pass

    def render(self) -> None:
        self.window_surface.blit(self.board_image, self.board_rect)

        for piece in self.pieces:
            piece.render()
