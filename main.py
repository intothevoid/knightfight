"""
Knight Fight is a Chess game written using pygame.
"""

from typing import Optional
import pygame
import sys

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

                            if piece_moved and original_pos != moved_pos:
                                # change turn
                                turn = (
                                    PieceColour.White
                                    if turn == PieceColour.Black
                                    else PieceColour.Black
                                )
                                play_sound("drop.mp3", sound_vol)
                            else:
                                play_sound("invalid_move.mp3", sound_vol)

                # update the display
                if board.state.game_over:
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
    font_size = config.APP_CONFIG["game"]["grid_font_size"]
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
