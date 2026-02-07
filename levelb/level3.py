# Level 3
import pygame
from blockt import dblocks, sblocks
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
        sblocks.create_sblock(200, 450),
        sblocks.create_sblock(500, 180),
        sblocks.create_sblock(720, 300),
    ]

    # Exit
    exit_rect = pygame.Rect(
        int(350 * SCALE),
        int(6 * SCALE),
        int(100 * SCALE),
        int(100 * SCALE)
    )

    return platform, blocks, exit_rect
