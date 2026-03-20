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


# --------------------------------------------------
# Block creation
# --------------------------------------------------

def create_xblocks(n, bound_rect):
    blocks = []
    for _ in range(n):
        x = random.randint(bound_rect.left, bound_rect.right - SIZE)
        y = random.randint(bound_rect.top, bound_rect.bottom - SIZE)

        blocks.append(_make_block(x, y, bound_rect))
    return blocks


def create_xblock(x, y, bound_rect):
    x = int(x * SCALE)
    y = int(y * SCALE)

    x = max(bound_rect.left, min(bound_rect.right - SIZE, x))
    y = max(bound_rect.top, min(bound_rect.bottom - SIZE, y))

    return _make_block(x, y, bound_rect)


def _make_block(x, y, bound_rect):
    return {
        "rect": pygame.Rect(x, y, SIZE, SIZE),
        "kind": "xblock",
        "dragging": False,
        "offset_x": 0,
        "offset_y": 0,
        "bound": bound_rect   
    }


# --------------------------------------------------
# Drag Logic (MATCHES DBLOCKS STYLE)
# --------------------------------------------------

def handle_mouse_down(blocks, mouse_x, mouse_y, button_pressed):
    if button_pressed:
        return

    for block in blocks:
        rect = block["rect"]
        if rect.collidepoint(mouse_x, mouse_y):
            block["dragging"] = True
            block["offset_x"] = rect.x - mouse_x
            block["offset_y"] = rect.y - mouse_y
            break


def update_drag(blocks, button_pressed):
    if button_pressed:
        return

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for block in blocks:
        if block.get("kind") != "xblock":
            continue

        if block.get("dragging"):
            bound = block["bound"]

            new_x = mouse_x + block["offset_x"]
            new_y = mouse_y + block["offset_y"]

            new_x = max(bound.left, min(bound.right - SIZE, new_x))
            new_y = max(bound.top, min(bound.bottom - SIZE, new_y))

            block["rect"].x = new_x
            block["rect"].y = new_y


def handle_mouse_up(blocks):
    for block in blocks:
        block["dragging"] = False


# --------------------------------------------------
# Hazard Logic
# --------------------------------------------------

def update_xblocks(blocks):
    for block in blocks:
        if block.get("kind") != "xblock":
            continue

        if player.colliderect(block["rect"]):
            reset_full_player_state()
            player.x = PLAYER_START_X
            player.y = PLAYER_START_Y
            return


# --------------------------------------------------
# Draw Bounding Box
# --------------------------------------------------

def draw_bounds(screen, blocks):
    if not blocks:
        return

    # Assume all xblocks share same bound
    bound = blocks[0]["bound"]
    pygame.draw.rect(screen, (0, 200, 255), bound, 3)