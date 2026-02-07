import random
import pygame
from config import NEW_HEIGHT, NEW_WIDTH, SCALE

# Base (unscaled) values
BASE_RECT_WIDTH = 170
BASE_RECT_HEIGHT = 10

# Screen size
WIDTH = NEW_WIDTH
HEIGHT = NEW_HEIGHT

# Scaled values
RECT_WIDTH = int(BASE_RECT_WIDTH * SCALE)
RECT_HEIGHT = int(BASE_RECT_HEIGHT * SCALE)


# --------------------------------------------------
# Block creation
# --------------------------------------------------

def create_blocks(n):
    blocks = []
    for _ in range(n):
        x = random.randint(0, WIDTH - RECT_WIDTH)
        y = random.randint(int(100 * SCALE), HEIGHT - RECT_HEIGHT - int(50 * SCALE))

        blocks.append({
            "rect": pygame.Rect(x, y, RECT_WIDTH, RECT_HEIGHT),
            "kind": "rect",
            "dragging": False,
            "offset_x": 0,
            "offset_y": 0
        })
    return blocks


def create_block(x, y):
    x = int(x * SCALE)
    y = int(y * SCALE)

    x = max(0, min(WIDTH - RECT_WIDTH, x))
    y = max(int(100 * SCALE), min(HEIGHT - RECT_HEIGHT - int(50 * SCALE), y))

    return {
        "rect": pygame.Rect(x, y, RECT_WIDTH, RECT_HEIGHT),
        "kind": "rect",
        "dragging": False,
        "offset_x": 0,
        "offset_y": 0
    }


# --------------------------------------------------
# Drag logic
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
        if block["dragging"]:
            new_x = mouse_x + block["offset_x"]
            new_y = mouse_y + block["offset_y"]

            new_x = max(0, min(WIDTH - RECT_WIDTH, new_x))
            new_y = max(0, min(HEIGHT - RECT_HEIGHT, new_y))

            block["rect"].x = new_x
            block["rect"].y = new_y


def handle_mouse_up(blocks):
    for block in blocks:
        block["dragging"] = False
