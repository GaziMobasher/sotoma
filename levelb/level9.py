# Level 4
import pygame
from blockt import dblocks, gblocks, xblocks, sblocks
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
        xblocks.create_xblock(300, 60),
        gblocks.create_gblock(400, 120),
        gblocks.create_gblock(400, 180),
        gblocks.create_gblock(400, 240),
        sblocks.create_sblock(160, 160)
    ]

    # Exit
    exit_rect = pygame.Rect(
        int(280 * SCALE),
        int(1 * SCALE),
        int(100 * SCALE),
        int(100 * SCALE)
    )

    return platform, blocks, exit_rect