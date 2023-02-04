"""
Playback module for the sound package.
"""

import pygame
from config import config


def play_sound(sound_file: str) -> None:
    """
    Play a sound from the assets folder
    """

    if config.APP_CONFIG["game"]["sound"] == False:
        return

    sound = pygame.mixer.Sound(f"assets/{sound_file}")
    sound.play()


def play_music(music_file: str) -> None:
    """
    Play a music from the assets folder
    """
    if config.APP_CONFIG["game"]["music"] == False:
        return

    pygame.mixer.music.load(f"assets/{music_file}")
    pygame.mixer.music.play(-1)
