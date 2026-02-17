import random
import pygame
from config import NEW_WIDTH, NEW_HEIGHT, SCALE
from player import (
    player,
    PLAYER_START_X,
    PLAYER_START_Y,
    reset_full_player_state
)


# --------------------------------------------------
# Constants
# --------------------------------------------------

BASE_RECT_SIZE = 70

WIDTH = NEW_WIDTH
HEIGHT = NEW_HEIGHT

SIZE = int(BASE_RECT_SIZE * SCALE)

MIN_Y = int(100 * SCALE)
MAX_Y = HEIGHT - SIZE - int(50 * SCALE)


# --------------------------------------------------
# Block creation
# --------------------------------------------------

def create_xblocks(n):
    blocks = []
    for _ in range(n):
        x = random.randint(0, WIDTH - SIZE)
        y = random.randint(MIN_Y, MAX_Y)

        blocks.append(_make_block(x, y))
    return blocks


def create_xblock(x, y):
    x = int(x * SCALE)
    y = int(y * SCALE)

    x = max(0, min(WIDTH - SIZE, x))
    y = max(MIN_Y, min(MAX_Y, y))

    return _make_block(x, y)


def _make_block(x, y):
    return {
        "rect": pygame.Rect(x, y, SIZE, SIZE),
        "kind": "xblock"
    }


# --------------------------------------------------
# Hazard Logic
# --------------------------------------------------


def update_xblocks(blocks):
    """
    Static blocks.
    If player touches one -> reset player to start platform.
    """

    for block in blocks:
        if block.get("kind") != "xblock":
            continue

        if player.colliderect(block["rect"]):

            # Reset full player physics + animation
            reset_full_player_state()

            # Move player back to starting platform
            player.x = PLAYER_START_X
            player.y = PLAYER_START_Y
            return
