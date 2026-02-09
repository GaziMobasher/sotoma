import random
import pygame
from config import NEW_HEIGHT, NEW_WIDTH, SCALE

# Base (unscaled)
BASE_DIAMETER = 20

# Screen size
WIDTH = NEW_WIDTH
HEIGHT = NEW_HEIGHT

# Scaled values
DIAMETER = int(BASE_DIAMETER * SCALE)
RADIUS = DIAMETER // 2


# --------------------------------------------------
# Sphere creation
# --------------------------------------------------

def create_sblocks(n):
    spheres = []
    for _ in range(n):
        x = random.randint(0, WIDTH - DIAMETER)
        y = random.randint(int(100 * SCALE), HEIGHT - DIAMETER - int(50 * SCALE))

        spheres.append({
            "rect": pygame.Rect(x, y, DIAMETER, DIAMETER),
            "kind": "sphere",
            "dragging": False,
            "offset_x": 0,
            "offset_y": 0
        })
    return spheres


def create_sblock(x, y):
    x = int(x * SCALE)
    y = int(y * SCALE)

    x = max(0, min(WIDTH - DIAMETER, x))
    y = max(int(100 * SCALE), min(HEIGHT - DIAMETER - int(50 * SCALE), y))

    return {
        "rect": pygame.Rect(x, y, DIAMETER, DIAMETER),
        "kind": "sphere",
        "dragging": False,
        "offset_x": 0,
        "offset_y": 0
    }


# --------------------------------------------------
# Drag logic (circle-accurate click)
# --------------------------------------------------

def handle_mouse_down(spheres, mouse_x, mouse_y, button_pressed):
    if button_pressed:
        return

    for sphere in spheres:
        rect = sphere["rect"]
        cx = rect.x + RADIUS
        cy = rect.y + RADIUS

        dx = mouse_x - cx
        dy = mouse_y - cy

        if dx * dx + dy * dy <= RADIUS * RADIUS:
            sphere["dragging"] = True
            sphere["offset_x"] = rect.x - mouse_x
            sphere["offset_y"] = rect.y - mouse_y
            break


def update_drag(spheres, button_pressed):
    if button_pressed:
        return

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for sphere in spheres:
        if sphere["dragging"]:
            new_x = mouse_x + sphere["offset_x"]
            new_y = mouse_y + sphere["offset_y"]

            new_x = max(0, min(WIDTH - DIAMETER, new_x))
            new_y = max(0, min(HEIGHT - DIAMETER, new_y))

            sphere["rect"].x = new_x
            sphere["rect"].y = new_y


def handle_mouse_up(spheres):
    for sphere in spheres:
        sphere["dragging"] = False
