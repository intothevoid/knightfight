"""
The board class to capture the state of the chess board.
"""

import random
from typing import Tuple, Optional, List
import pygame
import chess
from ai.engine import add_move_to_engine_state, square_to_position
from animation.animation import display_sprite_animation
from helpers.log import LOGGER
from knightfight.piece import Piece
from knightfight.state import BoardState
from config import config
from knightfight.types import PieceColour, GridPosition, PieceType
from ai.validation import is_move_valid
from sound.playback import play_sound


class Board:
    def __init__(self, window_surface: pygame.surface.Surface) -> None:
        board_size = config.APP_CONFIG["board"]["size"]
        board_image = config.APP_CONFIG["board"]["image"]

        self.sound_vol = config.APP_CONFIG["game"]["sound_vol"]
        self.window_surface = window_surface
        self.board_image = pygame.image.load(f"assets/{board_image}")
        self.board_rect = self.board_image.get_rect()
        self.board_rect.topleft = (0, 0)
        self.board_image = pygame.transform.scale(
            self.board_image, (board_size, board_size)
        )

        self.state = BoardState()

        # initialize the pieces
        self.init_pieces()

        # list of squares to highlight
        self.highlighted_squares: List[int] = []

        # status text
        self.status_text = ""
        self.status_text_delay = 0

    def init_pieces(self) -> None:
        """
        Initialize the pieces on the board
        """

        self.state.engine_state = chess.Board()
        LOGGER.info(f"Starting FEN: {self.state.engine_state.fen()})")

        # iterate through chess pieces and add them to the board
        board = self.state.engine_state
        print(board)

        for square in board.piece_map():
            piece = board.piece_at(square)
            if piece is not None:
                row, col = 7 - (square // 8), (square % 8)
                piece_pos_x = 40 + col * 90
                piece_pos_y = 40 + row * 90

                piece = Piece(
                    self.window_surface,
                    PieceType(chess.piece_name(piece.piece_type).capitalize()),
                    PieceColour("W" if piece.color == chess.WHITE else "B"),
                    piece_pos_x,  # x pos left
                    piece_pos_y,  # y pos top
                    GridPosition(7 - row, col),
                    square,
                )
                self.add_piece(piece)

        return

    def draw_grid(self) -> None:
        """
        Draw the grid on the board
        """
        # show grid if enabled in config
        if config.APP_CONFIG["game"]["show_grid"]:
            for row in range(8):
                for col in range(8):
                    rect = pygame.Rect(
                        40 + col * 90, 40 + row * 90, 90, 90
                    )  # x, y, width, height

                    pygame.draw.rect(
                        self.window_surface,
                        (255, 0, 0),
                        rect,
                        1,
                    )

    def draw_debug(self) -> None:
        # draw text with rect.left, rect.top
        font_name = config.APP_CONFIG["game"]["font_name"]
        font_size = config.APP_CONFIG["game"]["grid_font_size"]
        debug_font = pygame.font.Font(f"assets/{font_name}", font_size)

        # show grid if enabled in config
        if config.APP_CONFIG["game"]["show_debug"]:
            for row in range(8):
                for col in range(8):
                    rect = pygame.Rect(
                        45 + col * 90, 55 + row * 90, 90, 90
                    )  # x, y, width, height

                    debug_pos_text = debug_font.render(
                        f"{rect.left},{rect.top}", True, (255, 0, 0)
                    )
                    self.window_surface.blit(debug_pos_text, rect)

    def draw_positions(self) -> None:
        """
        Draw the positions on the board
        """
        # show grid position if enabled in config
        if config.APP_CONFIG["game"]["show_positions"]:
            font_name = config.APP_CONFIG["game"]["font_name"]
            font_size = config.APP_CONFIG["game"]["grid_font_size"]
            grid_font = pygame.font.Font(f"assets/{font_name}", font_size)
            for row in range(8):
                for col in range(8):
                    x = 40 + col * 90 + 5
                    y = 40 + row * 90 + 5

                    col_lbl = chr(ord("a") + col)
                    grid_pos_text = grid_font.render(
                        f"{col_lbl}{7-row+1}", True, (255, 0, 0)
                    )
                    self.window_surface.blit(
                        grid_pos_text,
                        (x, y),
                    )

    # draw row numbers and column letters
    def draw_labels(self) -> None:
        """
        Draw the labels on the board
        """
        # show grid position if enabled in config
        if config.APP_CONFIG["game"]["show_labels"]:
            font_name = config.APP_CONFIG["game"]["font_name"]
            font_size = config.APP_CONFIG["game"]["label_font_size"]
            grid_font = pygame.font.Font(f"assets/{font_name}", font_size)

            # draw row numbers
            for row in range(0, 8):
                x = 40 / 2 - 5
                y = 40 + row * 90 + 35

                grid_pos_text = grid_font.render(f"{7 - row + 1}", True, (0, 0, 0))
                self.window_surface.blit(
                    grid_pos_text,
                    (x, y),
                )

            # draw column letters
            for col in range(8):
                x = 40 + col * 90 + 40
                y = 800 - 35

                grid_pos_text = grid_font.render(f"{chr(97 + col)}", True, (0, 0, 0))
                self.window_surface.blit(
                    grid_pos_text,
                    (x, y),
                )

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
        original_pos = piece.grid_pos

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
            # update position
            piece.piece_rect.topleft = square_to_position(piece.square)

            return False

        # handle collision, remove the piece
        self.check_collision_remove(piece, new_pos, target_sq_piece)

        # move piece and update piece position
        if piece.move_to(self.get_grid_at(new_pos), self.state):
            self.state.changed_pieces.append(piece)

            # update engine state, only if the move is valid
            self.state.engine_state = add_move_to_engine_state(
                self.state.engine_state,
                original_pos,
                self.get_grid_at(new_pos),
                piece.piece_type,
            )

            if len(self.state.engine_state.move_stack) > 0:
                LOGGER.info(
                    f"Moved {piece.piece_colour.value} {piece.piece_type.value} {self.state.engine_state.move_stack[-1]}"
                )
            LOGGER.debug(f"\nBoard:\n{self.state.engine_state}")

            return True

        return False

    def check_collision_remove(self, piece, new_pos, target_sq_piece):
        """
        Handle collision between pieces
        """
        if (
            target_sq_piece
            and target_sq_piece.piece_colour != piece.piece_colour
            and is_move_valid(
                piece.grid_pos,
                self.get_grid_at(new_pos),
                self.state.engine_state,
            )
        ):
            self.remove_piece(target_sq_piece)
            self.state.killed_pieces.append(target_sq_piece)

            # play explosion animation
            display_sprite_animation(
                self.window_surface,
                "assets/explosion.png",
                12,
                target_sq_piece.piece_rect,
            )

            # check if king is killed
            if target_sq_piece.piece_type == PieceType.King:
                self.state.game_over = True
                self.state.winner = piece.piece_colour
                play_sound("explode.mp3", self.sound_vol)
                play_sound("game_over.mp3", self.sound_vol)
            else:
                play_sound("explode.mp3", self.sound_vol)

    def redraw_pieces(self):
        for piece in self.state.pieces:
            piece.render()

        # show dragged piece on top after all other pieces have been rendered
        if self.state.dragged_piece:
            self.state.dragged_piece.render()
        else:
            # redraw pieces that have changed if no piece is being dragged
            for piece in self.state.changed_pieces:
                piece.render()

        # update board state
        self.state.changed_pieces.clear()

    def render(self) -> None:
        # draw the board
        self.window_surface.blit(self.board_image, self.board_rect)

        # draw grid
        self.draw_grid()

        # draw labels
        self.draw_labels()

        # draw debug information
        self.draw_debug()

        # draw positions
        self.draw_positions()

        # redraw pieces
        self.redraw_pieces()

        # draw the highlight squares
        if len(self.highlighted_squares) > 0:
            self.highlight_squares()

        # draw status text
        if self.status_text:
            self.draw_status_text()

    def get_piece_at(self, pos: Tuple[int, int]) -> List[Piece]:
        # a square can contain multiple pieces when a piece is being dragged
        # over an existing piece
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
        row = 7 - (y - 40) // 90  # reverse as y axis is inverted in pygame

        return GridPosition(row, col)

    def highlight_squares(self):
        """
        Highlight squares from the list of highlighted squares
        """
        for square in self.highlighted_squares:
            # get the square position
            x, y = square_to_position(square)

            # draw the rectangle
            pygame.draw.rect(
                self.window_surface,
                (255, 0, 0),
                (x, y, 90, 90),
                5,
            )

    def add_highlight_square(self, square: chess.Square):
        """
        Add a square to the list of highlighted squares
        """
        self.highlighted_squares.append(square)

    def clear_highlight_squares(self):
        """
        Clear the list of highlighted squares
        """
        self.highlighted_squares.clear()

    def draw_status_text(self):
        """
        Draw the labels on the board
        """
        # show text to indicate cpu is thinking
        font_name = config.APP_CONFIG["game"]["font_name"]
        font = pygame.font.Font(f"assets/{font_name}", 16)
        text = font.render(self.status_text, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (
            config.APP_CONFIG["board"]["size"] / 2,
            15,
        )
        self.window_surface.blit(text, text_rect)
        pygame.display.update()

        # wait between 1-3 seconds before making move
        pygame.time.wait(self.status_text_delay)

        # reset
        self.status_text = ""
        self.status_text_delay = 0

    def set_status_text(self, text: str, delay: int = 0):
        """
        Set the status text
        """
        self.status_text = text
        self.status_text_delay = delay
