# Level 4
import pygame
from blockt import dblocks, sblocks, destroblocks
from config import SCALE


def load():
    # Main static platform
    platform = pygame.Rect(
        int(800),
        int(900),
        int(200 * SCALE),
        int(30 * SCALE)
    )

    # Rectangular draggable platforms
    blocks = [
        destroblocks.create_destroblock(200, 450),
        destroblocks.create_destroblock(500, 180),
    ]

    # Exit
    exit_rect = pygame.Rect(
        int(350 * SCALE),
        int(6 * SCALE),
        int(100 * SCALE),
        int(100 * SCALE)
    )

    return platform, blocks, exit_rect