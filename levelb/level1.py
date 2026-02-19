# Level 1
import pygame
from blockt import dblocks
from config import SCALE

def load():
    platform = pygame.Rect(800, 900, 160*SCALE, 30*SCALE)
    blocks = [
        dblocks.create_block(300, 90),
        dblocks.create_block(300, 270),
        dblocks.create_block(300, 180)
    ]

    exit_rect = pygame.Rect(
        int(550 * SCALE),
        int(10 * SCALE),
        int(100 * SCALE),
        int(100 * SCALE)
    )
    return platform, blocks, exit_rect
