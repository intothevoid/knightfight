"""
Package to manage sprite animations.
"""

import pygame
from typing import List, Tuple


import pygame


def display_sprite_animation(
    screen: pygame.surface.Surface,
    image_name: str,
    sprite_count: int,
    rect: pygame.rect.Rect,
):
    # Load the sprite sheet image
    sprite_sheet = pygame.image.load(image_name)

    # Get the individual frame dimensions
    frame_width = sprite_sheet.get_width() // sprite_count  # number of frames
    frame_height = sprite_sheet.get_height()

    # Create a list to store the individual frames
    frames = []

    # Cut the sprite sheet into individual frames and add to the list
    for i in range(sprite_count):
        frames.append(
            sprite_sheet.subsurface(
                pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            )
        )

    # Set the clock for controlling the animation speed
    clock = pygame.time.Clock()

    # Index to keep track of the current frame
    current_frame = 0

    while current_frame < sprite_count:

        # Display the current frame
        screen.blit(frames[current_frame], rect)

        # Update the display
        pygame.display.update()

        # Increment the current frame
        current_frame += 1

        # Control the animation speed
        clock.tick(24)
