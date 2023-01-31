"""
The board class to capture the state of the chess board.
"""

import pygame
from chess.piece import Piece
from config import config
from chess.types import PieceType, PieceColour


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
        for row in range(8):
            for col in range(8):
                if row in [0, 1]:
                    piece_type = PieceType.Pawn
                    piece_colour = PieceColour.Black
                elif row in [6, 7]:
                    piece_type = PieceType.Pawn
                    piece_colour = PieceColour.White
                else:
                    piece_type = PieceType.Empty
                    piece_colour = PieceColour.Empty

                if piece_type != PieceType.Empty:
                    piece_pos = (40 + col * 90, 40 + row * 90)
                    piece = Piece(self.window_surface, piece_type,
                                  piece_colour, piece_pos)

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

    def move_piece(self, piece: Piece, new_pos) -> None:
        piece.piece_pos = new_pos
        piece.piece_rect.topleft = new_pos

    def render(self) -> None:
        self.window_surface.blit(self.board_image, self.board_rect)

        for piece in self.pieces:
            piece.render()
