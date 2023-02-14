"""
Knight Fight is a Chess game written using pygame.
"""

import os
import sys
import traceback
import pygame
import chess

from helpers.conversions import grid_pos_to_move, grid_position_to_label
from ai.lookup import CHESS_SQUARE_TO_POS

from knightfight.board import Board
from knightfight.state import BoardState
from config import config
from knightfight.types import GridPosition, PieceColour, PieceType
from helpers.log import LOGGER
from sound.playback import play_music, play_sound
from ai.player import AIPlayer


BOARD_BK_COLOUR = (255, 255, 255)
BOARD_BK_COLOUR_BLACK = (0, 0, 0)

# Workaround to get Windows pygame to load audio correctly
# The pygame audio dll does not load correctly, this adds
# the pygame directory to the system path
if os.name == "nt":
    # pypy does not find the dlls, so we add package folder to PATH.
    pygame_dir = os.path.split(pygame.__file__)[0]
    os.environ["PATH"] = os.environ["PATH"] + ";" + pygame_dir
    # Fix for the bpo-36085 change in Python3.8 on Windows
    os.add_dll_directory(pygame_dir)


class KnightFight:
    def __init__(self):
        self.dragged_piece = None
        self.drag_offset = None

    def show_splash_screen(self, screen):
        """
        Show splash screen on new window
        """
        # load splash screen image
        splash_image = pygame.image.load("assets/images/logo.png")

        # set image size to 50% of board size
        splash_image = pygame.transform.scale(
            splash_image,
            (
                config.APP_CONFIG["board"]["size"],
                config.APP_CONFIG["board"]["size"],
            ),
        )

        splash_rect = splash_image.get_rect()
        splash_rect.center = (
            config.APP_CONFIG["board"]["size"] // 2,
            config.APP_CONFIG["board"]["size"] // 2,
        )

        # show splash screen
        screen.blit(splash_image, splash_rect)
        pygame.display.update()

    def run(self):
        # initialize pygame and load config
        pygame.init()
        config.read_config()

        # set up sound volume
        music_vol = config.APP_CONFIG["game"]["music_vol"]
        sound_vol = config.APP_CONFIG["game"]["sound_vol"]

        # set up the window
        board_size = config.APP_CONFIG["board"]["size"]
        screen = pygame.display.set_mode((board_size, board_size))
        screen.fill(BOARD_BK_COLOUR)

        # set window title
        pygame.display.set_caption("KNIGHT FIGHT")
        pygame.mouse.set_visible(True)

        # show splash screen
        # self.show_splash_screen(screen)

        # players
        p1_type = config.APP_CONFIG["game"]["player1"].lower().strip()
        p2_type = config.APP_CONFIG["game"]["player2"].lower().strip()

        # setup ai player and engines
        # max ai players = 2 cpu vs cpu
        ai = config.APP_CONFIG["cpu"]["ai"]  # use basic / piece_squares ai
        complexity = config.APP_CONFIG["cpu"]["complexity"]  # ai complexity
        engine_path = ""

        if ai == "stockfish":
            engine_path = config.APP_CONFIG["cpu"]["stockfish_path"]

        ai_white = AIPlayer(chess.WHITE, sound_vol, ai, complexity, engine_path)
        ai_black = AIPlayer(chess.BLACK, sound_vol, ai, complexity, engine_path)
        AI_PLAYERS = {
            PieceColour.White: ai_white,
            PieceColour.Black: ai_black,
        }
        cpu_delay = config.APP_CONFIG["cpu"]["delay"]  # delay between moves

        # setup board
        board = Board(screen)

        # track turn
        turn = PieceColour.White

        # play music
        ost = config.APP_CONFIG["game"]["soundtrack"]
        play_music(ost, music_vol)  # music volume

        try:
            # main loop
            # check if game is over
            game_over_flag = False
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # get last fen and save to config
                        fen = board.state.engine_state.fen()
                        config.APP_CONFIG["state"]["last_fen"] = str(fen)
                        config.save_config()
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # check if a piece is clicked
                        pos = pygame.mouse.get_pos()
                        try:
                            clicked_piece = board.get_piece_at(pos)[0]  # only one piece
                            if clicked_piece and clicked_piece.piece_colour == turn:
                                # save starting position and start drag-drop event
                                self.dragged_piece = clicked_piece
                                self.drag_offset = (
                                    pos[0] - clicked_piece.piece_rect.x,
                                    pos[1] - clicked_piece.piece_rect.y,
                                )
                            else:
                                play_sound("invalid_move.mp3", sound_vol)
                        except IndexError:
                            # no piece at position
                            pass
                    elif event.type == pygame.MOUSEMOTION:
                        # update piece position if drag drop is active
                        if self.dragged_piece:
                            # dragged piece to board state to allow rendering
                            # of piece on top of other pieces
                            board.state.dragged_piece = self.dragged_piece
                            pos = pygame.mouse.get_pos()
                            if self.drag_offset:
                                self.dragged_piece.piece_rect.x = (
                                    pos[0] - self.drag_offset[0]
                                )
                                self.dragged_piece.piece_rect.y = (
                                    pos[1] - self.drag_offset[1]
                                )
                    elif event.type == pygame.MOUSEBUTTONUP:
                        # end drag and drop event
                        if self.dragged_piece:
                            # update piece position on board
                            original_pos = self.dragged_piece.grid_pos
                            pos = pygame.mouse.get_pos()
                            piece_moved = board.move_piece(self.dragged_piece, pos)
                            moved_pos = self.dragged_piece.grid_pos
                            self.dragged_piece = None
                            board.state.dragged_piece = None
                            self.drag_offset = None

                            turn = self.handle_piece_moved(
                                board,
                                turn,
                                original_pos,
                                moved_pos,
                                piece_moved,
                            )
                    elif event.type == pygame.USEREVENT:
                        game_over(screen, board.state)
                        pygame.time.set_timer(pygame.USEREVENT, 0)  # Stop the timer

                # check if game is over
                if (
                    board.state.engine_state.is_game_over()
                    or board.state.engine_state.is_stalemate()
                    or board.state.engine_state.is_insufficient_material()
                    or board.state.engine_state.is_seventyfive_moves()
                    or board.state.engine_state.is_fivefold_repetition()
                    or board.state.engine_state.can_claim_fifty_moves()
                    or board.state.game_over == True
                ):
                    # pygame timer start to show game over screen
                    if not game_over_flag:
                        # show the initial game over screen, then show the
                        # final game over screen after 10 seconds
                        pygame.time.set_timer(pygame.USEREVENT, 10000)
                        game_over(screen, board.state, True)

                    # set game over flag
                    game_over_flag = True

                # if either player is cpu, make a move
                if (
                    (p1_type == "cpu" and turn == PieceColour.White)
                    or (p2_type == "cpu" and turn == PieceColour.Black)
                    and not game_over_flag
                ):
                    board.set_status_text("CPU is thinking...", cpu_delay)
                    board.render()

                    # get random move from list of legal moves
                    ai_moved = AI_PLAYERS[turn].move(board)
                    original_pos = AI_PLAYERS[turn].original_pos
                    moved_pos = AI_PLAYERS[turn].new_pos

                    if ai_moved and original_pos and moved_pos:
                        # change turn
                        turn = self.handle_piece_moved(
                            board,
                            turn,
                            original_pos,
                            moved_pos,
                            ai_moved,
                        )

                # update the display
                if not game_over_flag:
                    board.render()
                    pygame.display.update()

        except Exception as exc:
            # show stack trace
            LOGGER.error(f"Error: {exc} Stack trace: {traceback.format_exc()}")

    def handle_piece_moved(
        self,
        board: Board,
        turn: PieceColour,
        original_pos: GridPosition,
        moved_pos: GridPosition,
        piece_moved: bool,
    ):
        sound_vol = config.APP_CONFIG["game"]["sound_vol"]

        if piece_moved and original_pos != moved_pos:
            frompos = grid_position_to_label(original_pos)
            topos = grid_position_to_label(moved_pos)

            # clear any existing highlights
            board.clear_highlight_squares()
            board_copy = board.state.engine_state.copy()
            board_copy.pop()  # get rid of last move from copy so we can see if check on last move
            move = grid_pos_to_move(original_pos, moved_pos)

            # See if move gives check
            try:
                if board_copy.gives_check(move):
                    self.handle_check(
                        board, turn, float(sound_vol), frompos, topos, board_copy
                    )
            except AssertionError:
                # move is not legal
                LOGGER.info(f"Invalid move {frompos} -> {topos}!")

            # See if move gives checkmate
            if board.state.engine_state.is_checkmate():
                play_sound("check_mate.mp3", sound_vol)
                LOGGER.info(f"Checkmate from move {frompos} -> {topos}! GAME OVER!")
                board.state.game_over = True

            # change turn
            turn = (
                PieceColour.White
                if board.state.engine_state.turn
                else PieceColour.Black
            )

            play_sound("drop.mp3", sound_vol)
        else:
            play_sound("invalid_move.mp3", sound_vol)
        return turn

    def handle_check(
        self,
        board: Board,
        turn: PieceColour,
        sound_vol: float,
        frompos: str,
        topos: str,
        board_copy: chess.Board,
    ):
        play_sound("check.mp3", sound_vol)

        king_square = board_copy.king(
            # get king square for opposite colour
            True
            if turn == PieceColour.Black
            else False
        )

        # highlight square with red background for 5 seconds
        if king_square:
            board.add_highlight_square(king_square)

        LOGGER.info(f"King is in check from move {frompos} -> {topos}")


def game_over(screen: pygame.surface.Surface, state: BoardState, initial: bool = False):
    """
    Display game over screen
    """
    # set up font
    font_name = config.APP_CONFIG["game"]["font_name"]
    font = pygame.font.Font(f"assets/fonts/{font_name}", 72)
    board_size = config.APP_CONFIG["board"]["size"]

    winner_piece = None
    for piece in state.pieces:
        if piece.piece_type == PieceType.King:
            winner_piece = piece
            break

    # set up text
    text = font.render("Game Over", True, (255, 255, 255))
    text_blk = font.render("Game Over", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (
        board_size // 2,
        board_size // 2,
    )

    # set up font
    win_text = "White" if state.winner == PieceColour.White else "Black"
    font2 = pygame.font.Font(f"assets/fonts/{font_name}", 48)
    text2 = font2.render(f"{win_text} wins!", True, (255, 255, 255))
    text_rect2 = text2.get_rect()
    text_rect2.center = (
        board_size // 2,
        board_size // 2 + 80,
    )

    # show game over screen
    if not initial:
        screen.fill(BOARD_BK_COLOUR_BLACK)
        screen.blit(text, text_rect)
        screen.blit(text2, text_rect2)
        if winner_piece:
            winner_rect = winner_piece.piece_rect
            winner_rect.center = (
                board_size // 2,
                board_size // 2 - 100,
            )
            screen.blit(winner_piece.piece_image, winner_rect)
    else:
        screen.blit(text_blk, text_rect)

    pygame.display.update()


def start():
    chess = KnightFight()
    chess.run()


if __name__ == "__main__":
    start()
