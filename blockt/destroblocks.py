import random
import pygame
from config import NEW_WIDTH, NEW_HEIGHT, SCALE

# --------------------------------------------------
# Constants
# --------------------------------------------------

BASE_RECT_WIDTH = 50
BASE_RECT_HEIGHT = 50

WIDTH = NEW_WIDTH
HEIGHT = NEW_HEIGHT

RECT_WIDTH = int(BASE_RECT_WIDTH * SCALE)
RECT_HEIGHT = int(BASE_RECT_HEIGHT * SCALE)

MIN_Y = int(100 * SCALE)
MAX_Y = HEIGHT - RECT_HEIGHT - int(50 * SCALE)


# --------------------------------------------------
# Block creation
# --------------------------------------------------

def create_destroblocks(n):
    blocks = []
    for _ in range(n):
        x = random.randint(0, WIDTH - RECT_WIDTH)
        y = random.randint(MIN_Y, MAX_Y)

        blocks.append(_make_block(x, y))
    return blocks


def create_destroblock(x, y):
    x = int(x * SCALE)
    y = int(y * SCALE)

    x = max(0, min(WIDTH - RECT_WIDTH, x))
    y = max(MIN_Y, min(MAX_Y, y))

    return _make_block(x, y)


def _make_block(x, y):
    return {
        "rect": pygame.Rect(x, y, RECT_WIDTH, RECT_HEIGHT),
        "kind": "destro",
        "dragging": False,
        "offset_x": 0,
        "offset_y": 0,
        "destroyed": False,

        # breaking phase
        "breaking": False,
        "break_timer": 0,

        # NEW falling phase
        "falling": False,
        "fall_velocity": 0,
        "slide_velocity": 0
    }




# --------------------------------------------------
# Drag logic (same behavior as your normal blocks)
# --------------------------------------------------

def handle_mouse_down(blocks, mouse_x, mouse_y, button_pressed):
    if button_pressed:
        return

    for block in blocks:
        if block["destroyed"]:
            continue

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
        if not block["dragging"] or block["destroyed"]:
            continue

        new_x = mouse_x + block["offset_x"]
        new_y = mouse_y + block["offset_y"]

        new_x = max(0, min(WIDTH - RECT_WIDTH, new_x))
        new_y = max(MIN_Y, min(MAX_Y, new_y))

        block["rect"].x = new_x
        block["rect"].y = new_y


def handle_mouse_up(blocks):
    for block in blocks:
        block["dragging"] = False


# --------------------------------------------------
# Destruction logic
# --------------------------------------------------

def destroy_if_player_stands(blocks, player_rect, player_vel_y):
    """
    Destroy block if player is landing on it.
    player_vel_y must be passed in.
    """

    for block in blocks:
        if block["destroyed"]:
            continue

        block_rect = block["rect"]

        # Check horizontal overlap
        horizontal_overlap = (
            player_rect.right > block_rect.left and
            player_rect.left < block_rect.right
        )

        # Player is falling
        falling = player_vel_y >= 0

        # Player feet touching or slightly inside block top
        touching_top = (
            player_rect.bottom >= block_rect.top and
            player_rect.bottom <= block_rect.top + 10
        )

        if horizontal_overlap and falling and touching_top:
            block["destroyed"] = True



# --------------------------------------------------
# Utility
# --------------------------------------------------

def get_active_rects(blocks):
    """
    Use this for collision detection.
    Returns only blocks that are not destroyed.
    """
    return [b["rect"] for b in blocks if not b["destroyed"]]


def reset_destroblocks(blocks):
    """
    Call this on full level reset.
    """
    for block in blocks:
        block["destroyed"] = False

def update_destroblocks(blocks):
    current_time = pygame.time.get_ticks()

    for block in blocks:

        # Skip non-destro blocks
        if block.get("kind") != "destro":
            continue

        if block.get("destroyed"):
            continue

        # -------- BREAK TIMER --------
        if block.get("breaking") and not block.get("falling"):
            if current_time - block["break_timer"] >= 1500:
                block["falling"] = True

                import random
                block["slide_velocity"] = random.choice([-2, 2])

        # -------- FALLING PHYSICS --------
        if block.get("falling"):
            block["fall_velocity"] += 0.5
            block["rect"].y += block["fall_velocity"]
            block["rect"].x += block["slide_velocity"]

            if block["rect"].top > HEIGHT:
                block["destroyed"] = True

