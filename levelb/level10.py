# Level 4
import pygame
from blockt import dblocks, gblocks, xblocks, sblocks, destroblocks
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
        dblocks.create_block(45, 410),
        xblocks.create_xblock(600, 20),
        xblocks.create_xblock(450, 0),
        destroblocks.create_destroblock(45, 310),
        destroblocks.create_destroblock(45, 210),

    ]

    # Exit
    exit_rect = pygame.Rect(
        int(600 * SCALE),
        int(1 * SCALE),
        int(100 * SCALE),
        int(100 * SCALE)
    )

    return platform, blocks, exit_rect