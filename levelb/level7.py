# Level 4
import pygame
from blockt import dblocks, sblocks, destroblocks, xblocks
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

        xblocks.create_xblock(220, 220),
        xblocks.create_xblock(220, 320),
        xblocks.create_xblock(220, 120),
        destroblocks.create_destroblock(540, 540),
        dblocks.create_block(540, 30),
        sblocks.create_sblock(540, 170),
        sblocks.create_sblock(540, 210),
        
        
    ]

    # Exit
    exit_rect = pygame.Rect(
        int(90 * SCALE),
        int(250 * SCALE),
        int(100 * SCALE),
        int(100 * SCALE)
    )

    return platform, blocks, exit_rect