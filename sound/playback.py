"""
Playback module for the sound package.
"""

import pygame
from config import config


def play_sound(sound_file: str, volume: float = 1.0) -> None:
    """
    Play a sound from the assets folder
    """

    if config.APP_CONFIG["game"]["sound"] == False:
        return

    sound = pygame.mixer.Sound(f"assets/sounds/{sound_file}")
    sound.set_volume(volume)
    sound.play()


def play_music(music_file: str, volume: float = 1.0) -> None:
    """
    Play a music from the assets folder
    """
    if config.APP_CONFIG["game"]["music"] == False:
        return

    pygame.mixer.music.load(f"assets/sounds/{music_file}")
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)


def play_game_music() -> None:
    """
    Play the game music
    """
    ost = config.APP_CONFIG["game"]["soundtrack"]
    volume = config.APP_CONFIG["game"]["music_vol"]
    play_music(ost, volume)


def play_tense_music() -> None:
    """
    Play the tense music
    """
    volume = config.APP_CONFIG["game"]["music_vol"]
    play_music("tense.mp3", volume)


def play_title_music() -> None:
    """
    Play the title music
    """
    volume = config.APP_CONFIG["game"]["music_vol"]
    play_music("title.mp3", volume)
