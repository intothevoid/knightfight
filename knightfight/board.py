"""
The board class to capture the state of the chess board.
"""

from typing import Tuple, Optional, List
import pygame
import chess
from helpers.conversions import square_to_position
from helpers.pychess import add_move_to_engine_state
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
        self.board_image = pygame.image.load(f"assets/images/{board_image}")
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

        # for arrow from start to end square of last move
        self.last_move_arrow = None

        # for possible moves
        self.move_squares: chess.SquareSet = chess.SquareSet()

    def load_last_game(self) -> None:
        """
        Reset the board to the starting position
        """
        last_fen = config.APP_CONFIG["state"]["last_fen"]
        self.state.engine_state.reset()
        self.state = BoardState()
        self.init_pieces(last_fen)

    def undo_last_move(self) -> None:
        """
        Undo the last move
        """
        # save the current state
        last_state = self.state.engine_state

        # pop the last state - undo
        last_state.pop()

        # reset the board
        self.state = BoardState()

        # re-initialize the pieces
        self.init_pieces(last_state.fen())

    def init_pieces(self, last_fen: str = "") -> None:
        """
        Initialize the pieces on the board
        """

        # load the last state if requested
        self.state.engine_state = chess.Board(last_fen) if last_fen else chess.Board()
        LOGGER.info(f"Starting FEN: {self.state.engine_state.fen()})")

        # iterate through chess pieces and add them to the board
        board = self.state.engine_state
        LOGGER.info(f"Board\n{board}")

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
        debug_font = pygame.font.Font(f"assets/fonts/{font_name}", font_size)

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
            grid_font = pygame.font.Font(f"assets/fonts/{font_name}", font_size)
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
            grid_font = pygame.font.Font(f"assets/fonts/{font_name}", font_size)

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

    def get_piece(self, piece_pos) -> Optional[Piece]:
        for piece in self.state.pieces:
            if piece.piece_pos == piece_pos:
                return piece

        return None

    def populate_move_squares(self) -> None:
        """
        Populate the move squares for each piece
        """
        show_moves = config.APP_CONFIG["board"]["show_possible_moves"]
        if not show_moves:
            return

        # get the square of the piece
        if self.state.dragged_piece:
            self.move_squares = self.state.engine_state.attacks(
                self.state.dragged_piece.square
            )

        # manually add moves for pawns
        if (
            self.state.dragged_piece
            and self.state.dragged_piece.piece_type == PieceType.Pawn
        ):
            # get the pawn moves
            pawn_moves = self.state.engine_state.pseudo_legal_moves

            # add the pawn moves to the possible move squares
            for move in pawn_moves:
                if move.from_square == self.state.dragged_piece.square:
                    self.move_squares.add(move.to_square)

        # clear squares which are not legal moves
        if len(self.move_squares) > 0:
            for square in self.move_squares:
                move = chess.Move(self.state.dragged_piece.square, square)
                if move not in self.state.engine_state.legal_moves:
                    self.move_squares.remove(square)

    def clear_move_squares(self) -> None:
        """
        Clear the move squares
        """
        self.move_squares.clear()

    def move_piece(
        self, piece: Piece, new_pos: Tuple[int, int], animate: bool = False
    ) -> bool:
        # check if target square is occupied
        pieces = self.get_piece_at(new_pos)
        target_sq_piece = None
        original_pos = piece.grid_pos
        start_square = piece.square
        end_square = piece.square

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
        if piece.move_to(self.get_grid_at(new_pos), self.state, animate):
            self.state.changed_pieces.append(piece)

            # update engine state, only if the move is valid
            self.state.engine_state = add_move_to_engine_state(
                self.state.engine_state,
                original_pos,
                self.get_grid_at(new_pos),
                piece.piece_type,
            )

            # update end square
            end_square = piece.square

            # update last move arrow
            self.last_move_arrow = (start_square, end_square)

            if len(self.state.engine_state.move_stack) > 0:
                LOGGER.info(
                    f"Moved {piece.piece_colour.value} {piece.piece_type.value} {self.state.engine_state.move_stack[-1]}"
                )
            LOGGER.debug(f"\nBoard:\n{self.state.engine_state}")

            return True
        else:
            # reset position
            piece.piece_rect.topleft = square_to_position(piece.square)

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
                "assets/images/explosion.png",
                12,
                target_sq_piece.piece_rect,
            )

            # play explosion sound
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
        # draw last move arrow
        if self.last_move_arrow:
            self.draw_last_move_arrow()

        # draw possible move squares
        if len(self.move_squares) > 0:
            self.draw_move_squares()

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
        font = pygame.font.Font(f"assets/fonts/{font_name}", 16)
        text = font.render(self.status_text, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (
            config.APP_CONFIG["board"]["size"] / 2,
            15,
        )
        self.window_surface.blit(text, text_rect)
        pygame.display.update()

        # wait for status_text_delay seconds before clearing the text
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

    # draw the last move arrow
    def draw_last_move_arrow(self):
        if self.last_move_arrow:
            start_pos = square_to_position(self.last_move_arrow[0])
            end_pos = square_to_position(self.last_move_arrow[1])

            # draw arrow
            self.draw_arrow(
                (
                    start_pos[0] + 45,
                    start_pos[1] + 45,
                ),  # add 45 to get the center of the square
                (
                    end_pos[0] + 45,
                    end_pos[1] + 45,
                ),  # add 45 to get the center of the square
                (21, 26, 0),
                1,
            )

    # draw an arrow
    def draw_arrow(self, start_pos, end_pos, colour=(192, 192, 192), width=1):
        # draw small circle at start position
        pygame.draw.circle(
            self.window_surface,
            colour,
            start_pos,
            5,
        )

        # draw small circle at end position
        pygame.draw.circle(
            self.window_surface,
            colour,
            end_pos,
            5,
        )

        # draw line
        pygame.draw.line(
            self.window_surface,
            colour,
            start_pos,
            end_pos,
            width,
        )

    def draw_move_squares(self):
        """
        Draw the move squares as circles
        """
        for square in self.move_squares:
            x, y = square_to_position(square)

            # draw the circle
            pygame.draw.circle(
                self.window_surface,
                (0, 0, 0),
                (x + 45, y + 45),
                5,
            )
