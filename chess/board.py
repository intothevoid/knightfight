"""
The board class to capture the state of the chess board.
"""

import pygame
from typing import Tuple, Optional, List
from chess.piece import Piece
from chess.state import BoardState
from config import config
from chess.types import PieceColour, GridPosition
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

        # maintain state i.e. a list of pieces on the board
        self.state = BoardState()

        # initialize the pieces
        self.init_pieces()

    def init_pieces(self) -> None:
        """
        Initialize the pieces on the board
        """
        for piece_type, positions in self.state.get_starting_positions().items():
            for row, col in positions:
                piece_colour = PieceColour.Black if row in [0, 1] else PieceColour.White
                piece_pos = (40 + col * 90, 40 + row * 90)
                piece = Piece(
                    self.window_surface,
                    piece_type,
                    piece_colour,
                    piece_pos,
                    GridPosition(row, col),
                )
                self.add_piece(piece)

    def add_piece(self, piece: Piece) -> None:
        self.state.pieces.append(piece)

    def remove_piece(self, piece: Piece) -> None:
        # remove piece from the list
        # we delete it this way because a remove by value causes errors
        for i, p in enumerate(self.state.pieces):
            if p == piece:
                del self.state.pieces[i]
                break

    def get_piece(self, piece_pos) -> Optional[Piece | None]:
        for piece in self.state.pieces:
            if piece.piece_pos == piece_pos:
                return piece

        return None

    def move_piece(self, piece: Piece, new_pos: Tuple[int, int]) -> bool:
        # check if target square is occupied
        pieces = self.get_piece_at(new_pos)
        target_sq_piece = None

        # if piece gets detected at the target square
        if len(pieces) > 1:
            if pieces[0] == piece:
                target_sq_piece = pieces[1]
            else:
                target_sq_piece = pieces[0]
        else:
            target_sq_piece = pieces[0] if len(pieces) == 1 else None

        if (
            target_sq_piece
            and target_sq_piece != piece
            and target_sq_piece.piece_colour == piece.piece_colour
        ):
            # can't move to occupied square of same color
            # go back to old position
            piece.piece_rect.topleft = (
                40 + piece.grid_pos.col * 90,
                40 + piece.grid_pos.row * 90,
            )
            return False

        # handle collision, remove the piece
        if (
            target_sq_piece
            and target_sq_piece.piece_colour != piece.piece_colour
            and is_move_valid(
                piece.grid_pos,
                self.get_grid_at(new_pos),
                piece.piece_type,
                piece.piece_colour,
                self.state,
            )
        ):
            self.remove_piece(target_sq_piece)
            self.state.killed_pieces.append(target_sq_piece)

        # update piece position
        piece.move_to(self.get_grid_at(new_pos), self.state)
        self.state.changed_pieces.append(piece)
        return True

    def redraw_pieces(self):
        for piece in self.state.pieces:
            piece.render()
        for piece in self.state.changed_pieces:
            piece.render()

        # update board state
        self.state.update_board_state()
        self.state.changed_pieces.clear()

    def render(self) -> None:
        self.window_surface.blit(self.board_image, self.board_rect)

        # redraw pieces
        self.redraw_pieces()

    def get_piece_at(self, pos: Tuple[int, int]) -> List[Piece]:
        # a square can contain multiple pieces when a piece is being dragged over an existing piece
        pieces = []

        for piece in self.state.pieces:
            if piece.piece_rect.collidepoint(pos):
                pieces.append(piece)

        return pieces

    def get_grid_at(self, pos: Tuple[int, int]) -> GridPosition:
        x, y = pos

        if x < 40 or y < 40:  # margin on left is 40 pixels
            return GridPosition(-1, -1)
        if x > 740 or y > 740:  # margin on right is 40 pixels
            return GridPosition(-1, -1)

        col = (x - 40) // 90  # each square is 90 pixels
        row = (y - 40) // 90

        return GridPosition(row, col)
