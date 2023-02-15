from typing import Tuple
import pygame

from sound.playback import play_title_music
from knightfight.types import TitleChoice


def main_menu(config: dict) -> TitleChoice:
    board_size = config["board"]["size"]
    pygame.init()
    screen = pygame.display.set_mode((board_size, board_size))
    pygame.display.set_caption("KNIGHT FIGHT")

    # load splash screen image
    splash_image = pygame.image.load("assets/images/logo.png")

    # play title music
    play_title_music()

    # set image size to 50% of board size
    splash_image = pygame.transform.scale(
        splash_image,
        (
            board_size,
            board_size,
        ),
    )

    splash_rect = splash_image.get_rect()
    splash_rect.center = (
        board_size / 2,
        board_size / 2,
    )

    # show splash screen
    pygame.display.update()

    # draw menu options
    font_name = config["game"]["font_name"]
    font = pygame.font.Font(f"assets/fonts/{font_name}", 32)
    game_name_font = pygame.font.Font(f"assets/fonts/{font_name}", 84)

    # Game name static text
    game_name_text = game_name_font.render("KNIGHT FIGHT", True, (0, 0, 0))
    game_name_rect = game_name_text.get_rect(
        center=(board_size / 2 + 10, board_size - (board_size / 12))
    )

    # Play menu option
    play_text = font.render("New Game", True, (0, 0, 0))
    play_rect = play_text.get_rect(center=(board_size - (board_size / 6), 50))

    # Load menu option
    load_text = font.render("Load Game", True, (0, 0, 0))
    load_rect = load_text.get_rect(center=(board_size - (board_size / 6), 100))

    # Quit menu option
    quit_text = font.render("Quit", True, (0, 0, 0))
    quit_rect = quit_text.get_rect(center=(board_size - (board_size / 6), 150))

    # for flashing title text
    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
        (0, 255, 255),
        (255, 255, 255),
    ]
    clock = pygame.time.Clock()
    color_index = 0
    color_time = 0
    text_color = colors[color_index]

    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    # start game
                    return TitleChoice.New
                elif load_rect.collidepoint(event.pos):
                    # load game
                    return TitleChoice.Load
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()

        # draw menu screen
        screen.fill((0, 0, 0))
        screen.blit(splash_image, splash_rect)
        # screen.blit(game_name_text, game_name_rect)
        screen.blit(play_text, play_rect)
        screen.blit(load_text, load_rect)
        screen.blit(quit_text, quit_rect)

        # Change the color of the text every 200 milliseconds
        if pygame.time.get_ticks() - color_time > 200:
            color_index = (color_index + 1) % len(colors)
            color_time = pygame.time.get_ticks()
            text_color = colors[color_index]

        # flash title text
        flash_title_text(
            screen,
            game_name_font,
            game_name_rect,
            text_color,
        )

        pygame.display.flip()
        clock.tick(60)

        pygame.display.update()


def flash_title_text(
    screen: pygame.surface.Surface,
    font: pygame.font.Font,
    text_rect: pygame.rect.Rect,
    text_color: Tuple[int, int, int],
):
    text = font.render("KNIGHT FIGHT", True, (255, 255, 255))

    # Draw the text on the screen
    text = font.render("KNIGHT FIGHT", True, text_color)
    screen.blit(text, text_rect)
