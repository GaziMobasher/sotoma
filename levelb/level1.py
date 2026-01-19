# Level 1
import pygame
from blockt import dblocks
from config import SCALE

def load():
    platform = pygame.Rect(800, 900, 160*SCALE, 30*SCALE)
    blocks = [
        dblocks.create_block(600, 30),
        dblocks.create_block(450, 270),
        dblocks.create_block(220, 180)
    ]
    return platform, blocks
