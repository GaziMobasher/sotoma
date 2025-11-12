# Level 2
import pygame
from blockt import dblocks

def load():
    platform = pygame.Rect(300, 550, 200, 30)
    blocks = [
        dblocks.create_block(100, 300),
        dblocks.create_block(300, 200),

    ]
    return platform, blocks
