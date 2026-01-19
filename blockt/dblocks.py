import random
import pygame
from config import NEW_HEIGHT, NEW_WIDTH, SCALE

# Base (unscaled) values

BASE_RECT_WIDTH = 170
BASE_RECT_HEIGHT = 10

# Scaled values
WIDTH = NEW_WIDTH
HEIGHT = NEW_HEIGHT
rect_width = int(BASE_RECT_WIDTH * SCALE)
rect_height = int(BASE_RECT_HEIGHT * SCALE)


# Initialize draggable blocks
# For multiple blocks random scatter 
def create_blocks(n):
    rectangles = []
    for _ in range(n):
        rect_x = random.randint(0, WIDTH - rect_width)
        rect_y = random.randint(int(100 * SCALE), HEIGHT - rect_height - int(50 * SCALE))
        rectangles.append({
            "x": rect_x,
            "y": rect_y,
            "dragging": False,
            "offset_x": 0,
            "offset_y": 0
        })
    return rectangles


# For a single block at a certain position
def create_block(x, y):
    # Scale input position
    x = int(x * SCALE)
    y = int(y * SCALE)

    # Constrain the x and y coordinates to be within the screen
    x = max(0, min(WIDTH - rect_width, x))
    y = max(int(100 * SCALE), min(HEIGHT - rect_height - int(50 * SCALE), y))
    
    return {
        "x": x,
        "y": y,
        "dragging": False,
        "offset_x": 0,
        "offset_y": 0
    }


# Rectangle returner (CRITICAL: scaled rect)
def get_block_rect(rect):
    return pygame.Rect(rect["x"], rect["y"], rect_width, rect_height)


# Drag logic
def update_drag(rectangles, button_pressed):
    if not button_pressed:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for rect in rectangles:
            if rect["dragging"]:
                new_x = mouse_x + rect["offset_x"]
                new_y = mouse_y + rect["offset_y"]

                rect["x"] = max(0, min(WIDTH - rect_width, new_x))
                rect["y"] = max(0, min(HEIGHT - rect_height, new_y))


# Handle MOUSEBUTTONDOWN
def handle_mouse_down(rectangles, mouse_x, mouse_y, button_pressed):
    if not button_pressed:
        for rect in rectangles:
            if (
                rect["x"] <= mouse_x <= rect["x"] + rect_width and
                rect["y"] <= mouse_y <= rect["y"] + rect_height
            ):
                rect["dragging"] = True
                rect["offset_x"] = rect["x"] - mouse_x
                rect["offset_y"] = rect["y"] - mouse_y


# Handle MOUSEBUTTONUP
def handle_mouse_up(rectangles):
    for rect in rectangles:
        rect["dragging"] = False