# Level 2
import pygame
from blockt import dblocks
from config import SCALE

def load():
    platform = pygame.Rect(800, 900, 160*SCALE, 30*SCALE)
    blocks = [
        dblocks.create_block(100, 300),
        dblocks.create_block(300, 200),

    ]
    return platform, blocks
