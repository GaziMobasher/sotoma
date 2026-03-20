# Level 3
import pygame
from blockt import dblocks, sblocks, xblocks
from config import SCALE


def load():
    platform = pygame.Rect(
        int(800),
        int(900),
        int(160 * SCALE),
        int(30 * SCALE)
    )

    blocks = [
        sblocks.create_sblock(200, 450),
        sblocks.create_sblock(500, 180),
    ]

    # XBLOCK SETUP
    bound_rect = pygame.Rect(
        int(250 * SCALE),
        int(70 * SCALE),
        int(300 * SCALE),
        int(90 * SCALE)
    )

    xblock_list = [
        xblocks.create_xblock(150, 250, bound_rect),
        xblocks.create_xblock(300, 300, bound_rect),
    ]

    exit_rect = pygame.Rect(
        int(350 * SCALE),
        int(6 * SCALE),
        int(100 * SCALE),
        int(100 * SCALE)
    )

    return platform, blocks + xblock_list, exit_rect