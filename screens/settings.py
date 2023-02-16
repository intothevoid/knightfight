import sys
import pygame
import json
import pygame


def settings_screen(screen: pygame.surface.Surface, config: dict):
    BOARD_SIZE = config["board"]["size"]
    TRANSPARENT_BLACK = (0, 0, 0, 128)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    font = pygame.font.Font(None, 28)
    font_height = font.get_height()

    # Create a black translucent rectangle
    settings_rect = pygame.Surface((BOARD_SIZE, BOARD_SIZE), pygame.SRCALPHA)
    settings_rect.fill(TRANSPARENT_BLACK)

    # Blit the black rectangle on the screen
    screen.blit(
        settings_rect,
        (BOARD_SIZE // 2 - BOARD_SIZE // 2, BOARD_SIZE // 2 - BOARD_SIZE // 2),
    )

    config_text = json.dumps(config, indent=4)
    lines = config_text.split("\n")
    y = font_height
    for line in lines:
        text = font.render(line, True, (WHITE))
        screen.blit(text, (20, y))
        y += font_height

    edit_font = pygame.font.Font(None, 28)
    edit_button = pygame.Rect(0, 0, 200, 50)
    edit_button.center = (screen.get_width() // 2, screen.get_height() - 50)
    pygame.draw.rect(screen, BLACK, edit_button)
    text = edit_font.render("Edit", True, (WHITE))
    draw_edit_test(screen, text, edit_button)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    return
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                if edit_button.collidepoint(event.pos):
                    pygame.draw.rect(screen, RED, edit_button)
                    draw_edit_test(screen, text, edit_button)
                else:
                    pygame.draw.rect(screen, BLACK, edit_button)
                    draw_edit_test(screen, text, edit_button)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if edit_button.collidepoint(event.pos):
                    # get working directory
                    import os

                    cwd = os.getcwd()

                    # open config file in default text editor
                    if sys.platform == "win32":
                        os.system(f"notepad {cwd}/config.yml")
                    elif sys.platform == "linux":
                        os.system(f"xdg-open {cwd}/config.yml")
                    elif sys.platform == "darwin":
                        os.system(f"open {cwd}/config.yml")
                else:
                    # user clicked outside of the edit button
                    return

        pygame.display.update()


def draw_edit_test(screen, text, edit_button):
    screen.blit(
        text,
        (
            edit_button.centerx - text.get_width() // 2,
            edit_button.centery - text.get_height() // 2,
        ),
    )
