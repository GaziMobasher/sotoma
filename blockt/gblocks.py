# gblocks.py
import pygame
from config import NEW_WIDTH, NEW_HEIGHT, SCALE

BASE_RECT_WIDTH = 120
BASE_RECT_HEIGHT = 20

WIDTH = NEW_WIDTH
HEIGHT = NEW_HEIGHT

RECT_WIDTH = int(BASE_RECT_WIDTH * SCALE)
RECT_HEIGHT = int(BASE_RECT_HEIGHT * SCALE)



# --------------------
# Creation
# --------------------

def create_gblock(x, y):

    x = int(x * SCALE)
    y = int(y * SCALE)

    x = max(0, min(WIDTH - RECT_WIDTH, x))
    y = max(int(100 * SCALE), min(HEIGHT - RECT_HEIGHT - int(50 * SCALE), y))

    return {
        "rect": pygame.Rect(x, y, RECT_WIDTH, RECT_HEIGHT),
        "kind": "goo",
        "dragging": False,
        "offset_x": 0,
        "offset_y": 0
    }


def create_gblocks(n):
    import random
    blocks = []

    MIN_Y = int(100 * SCALE)
    MAX_Y = HEIGHT - RECT_HEIGHT - int(50 * SCALE)

    for _ in range(n):
        x = random.randint(0, WIDTH - RECT_WIDTH)
        y = random.randint(MIN_Y, MAX_Y)
        blocks.append(create_gblock(x, y))

    return blocks





# --------------------
# Drag Logic
# --------------------

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
        if not block.get("dragging"):
            continue

        block["rect"].x = mouse_x + block["offset_x"]
        block["rect"].y = mouse_y + block["offset_y"]


def handle_mouse_up(blocks):
    for block in blocks:
        block["dragging"] = False
