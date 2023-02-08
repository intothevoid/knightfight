"""
Knight Fight is a Chess game written using pygame.
"""

import random
import sys
import time
import pygame
import chess
from ai.engine import grid_pos_to_move, grid_position_to_label
from ai.lookup import CHESS_SQUARE_TO_POS

from knightfight.board import Board
from knightfight.state import BoardState
from config import config
from knightfight.types import PieceColour, PieceType
from helpers.log import LOGGER
from sound.playback import play_music, play_sound

BOARD_BK_COLOUR = (255, 255, 255)
BOARD_BK_COLOUR_BLACK = (0, 0, 0)


class KnightFight:
    def __init__(self):
        self.dragged_piece = None
        self.drag_offset = None

    def show_splash_screen(self, screen):
        """
        Show splash screen on new window
        """
        # load splash screen image
        splash_image = pygame.image.load("assets/logo.png")

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

        # show splash screen for 3 seconds
        pygame.time.delay(3000)

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

        pygame.display.set_caption(
            "Knight Fight - https://github.com/intothevoid/knightfight"
        )
        pygame.mouse.set_visible(True)

        # show splash screen
        # self.show_splash_screen(screen)

        # players
        cpu_enabled = config.APP_CONFIG["game"]["cpu_enabled"]
        no_players = config.APP_CONFIG["game"]["players"]

        # setup board
        board = Board(screen)

        # track turn
        turn = PieceColour.White

        # play music
        ost = config.APP_CONFIG["game"]["soundtrack"]
        play_music(ost, music_vol)  # music volume

        try:
            # main loop
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
                            frompos = grid_position_to_label(original_pos)
                            topos = grid_position_to_label(moved_pos)

                            if piece_moved and original_pos != moved_pos:
                                # clear any existing highlights
                                board.clear_highlight_squares()
                                board_copy = board.state.engine_state.copy()
                                board_copy.pop()  # get rid of last move so we can see if check on last move
                                move = grid_pos_to_move(original_pos, moved_pos)

                                # See if move gives check
                                if board_copy.gives_check(move):
                                    play_sound("check.mp3", sound_vol)

                                    king_square = board_copy.king(
                                        True if turn == PieceColour.Black else False
                                    )

                                    # highlight square with red background for 5 seconds
                                    if king_square:
                                        board.add_highlight_square(king_square)

                                    LOGGER.info(
                                        f"King is in check from move {frompos} -> {topos}"
                                    )

                                # See if move gives check
                                if board.state.engine_state.is_check():
                                    play_sound("check.mp3", sound_vol)
                                    LOGGER.info(
                                        f"King is in check from move {frompos} -> {topos}"
                                    )

                                # See if move gives checkmate
                                if board.state.engine_state.is_checkmate():
                                    play_sound("check_mate.mp3", sound_vol)
                                    LOGGER.info(
                                        f"Checkmate from move {frompos} -> {topos}! GAME OVER"
                                    )
                                    game_over(screen, board.state)

                                # change turn
                                turn = (
                                    PieceColour.White
                                    if board.state.engine_state.turn
                                    else PieceColour.Black
                                )
                                play_sound("drop.mp3", sound_vol)
                            else:
                                play_sound("invalid_move.mp3", sound_vol)

                # if colour is black and cpu is enabled, make a move
                # if cpu is enabled and 2 players, make a move i.e. both players are cpu
                if (
                    cpu_enabled and (turn == PieceColour.Black and no_players == 1)
                ) or (cpu_enabled and no_players == 2):
                    board.set_status_text("CPU is thinking...", 1000)
                    board.render()

                    # get random move from list of legal moves
                    move = random.choice(list(board.state.engine_state.legal_moves))
                    to_square = move.to_square
                    from_square = move.from_square

                    # get piece
                    board.state.engine_state.piece_at(move.from_square)
                    moved_piece = None
                    for piece in board.state.pieces:
                        if piece.square == from_square:
                            moved_piece = piece

                    new_pos = CHESS_SQUARE_TO_POS[to_square]
                    if moved_piece:
                        piece_moved = board.move_piece(moved_piece, new_pos)
                        if piece_moved:
                            play_sound("drop.mp3", sound_vol)
                        else:
                            play_sound("invalid_move.mp3", sound_vol)
                    else:
                        LOGGER.error(f"Piece not found at square {from_square}")

                    # change turn
                    turn = (
                        PieceColour.White
                        if board.state.engine_state.turn
                        else PieceColour.Black
                    )

                    # clear any existing highlights
                    board.clear_highlight_squares()

                # update the display
                if board.state.engine_state.is_game_over():
                    game_over(screen, board.state)
                else:
                    board.render()
                    pygame.display.update()

        except Exception as exc:
            LOGGER.error(exc)


# function to blank the screen and display game over message
def game_over(screen: pygame.surface.Surface, state: BoardState):
    # set up font
    font_name = config.APP_CONFIG["game"]["font_name"]
    font = pygame.font.Font(f"assets/{font_name}", 72)

    # draw image on screen at location config.APP_CONFIG["board"]["size"] // 2, config.APP_CONFIG["board"]["size"] // 2
    winner_piece = None
    for piece in state.pieces:
        if piece.piece_type == PieceType.King:
            winner_piece = piece
            break

    # set up text
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (
        config.APP_CONFIG["board"]["size"] // 2,
        config.APP_CONFIG["board"]["size"] // 2,
    )

    # set up font
    win_text = "White" if state.winner == PieceColour.White else "Black"
    font2 = pygame.font.Font(f"assets/{font_name}", 48)
    text2 = font2.render(f"{win_text} wins!", True, (255, 255, 255))
    text_rect2 = text2.get_rect()
    text_rect2.center = (
        config.APP_CONFIG["board"]["size"] // 2,
        config.APP_CONFIG["board"]["size"] // 2 + 80,
    )

    # show game over screen
    screen.fill(BOARD_BK_COLOUR_BLACK)
    screen.blit(text, text_rect)
    screen.blit(text2, text_rect2)
    if winner_piece:
        winner_rect = winner_piece.piece_rect
        winner_rect.center = (
            config.APP_CONFIG["board"]["size"] // 2,
            config.APP_CONFIG["board"]["size"] // 2 - 100,  # 100 pixels above text
        )
        screen.blit(winner_piece.piece_image, winner_rect)
    pygame.display.update()


def start():
    chess = KnightFight()
    chess.run()


if __name__ == "__main__":
    start()
