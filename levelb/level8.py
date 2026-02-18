# Level 4
import pygame
from blockt import dblocks, gblocks
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
        gblocks.create_gblock(150, 260),
        gblocks.create_gblock(280, 260)
    ]

    # Exit
    exit_rect = pygame.Rect(
        int(90 * SCALE),
        int(80 * SCALE),
        int(100 * SCALE),
        int(100 * SCALE)
    )

    return platform, blocks, exit_rect