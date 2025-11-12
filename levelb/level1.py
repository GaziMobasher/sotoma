# Level 1
import pygame
from blockt import dblocks

def load():
    platform = pygame.Rect(300, 550, 200, 30)
    blocks = [
        dblocks.create_block(600, 30),
        dblocks.create_block(450, 270),
        dblocks.create_block(220, 180)
    ]
    return platform, blocks
