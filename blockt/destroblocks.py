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

SHAKE_INTENSITY = int(3 * SCALE)  # max pixels to shake
SHAKE_DURATION = 500  # milliseconds


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

        # drag
        "dragging": False,
        "offset_x": 0,
        "offset_y": 0,

        # position memory
        "original_x": x,
        "original_y": y,

        # states
        "state": "idle",  # idle, breaking, falling, respawning

        # timers
        "break_timer": 0,
        "respawn_timer": 0,
        "protect_timer": 0,
        "shake_timer": 0,   # new timer for shaking

        # physics
        "fall_velocity": 0,
        "slide_velocity": 0,

        # protection
        "respawn_protected": False,

        # shake offset
        "shake_offset": 0
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
        if not block["dragging"]:
            continue
        new_x = mouse_x + block["offset_x"]
        new_y = mouse_y + block["offset_y"]
        new_x = max(0, min(WIDTH - RECT_WIDTH, new_x))
        new_y = max(MIN_Y, min(MAX_Y, new_y))
        block["rect"].x = new_x
        block["rect"].y = new_y


def handle_mouse_up(blocks):
    for block in blocks:
        if block["dragging"]:
            block["original_x"] = block["rect"].x
            block["original_y"] = block["rect"].y
        block["dragging"] = False


# --------------------------------------------------
# Destruction logic
# --------------------------------------------------

def destroy_if_player_stands(blocks, player_rect, player_vel_y):
    for block in blocks:
        if block["state"] != "idle":
            continue

        rect = block["rect"]

        horizontal_overlap = (
            player_rect.right > rect.left and
            player_rect.left < rect.right
        )

        falling = player_vel_y >= 0

        touching_top = (
            player_rect.bottom >= rect.top and
            player_rect.bottom <= rect.top + 10
        )

        if horizontal_overlap and falling and touching_top:
            block["state"] = "breaking"
            now = pygame.time.get_ticks()
            block["break_timer"] = now
            block["shake_timer"] = now


# --------------------------------------------------
# Utility
# --------------------------------------------------

def get_active_rects(blocks):
    return [b["rect"] for b in blocks if b["state"] != "falling"]


def reset_destroblocks(blocks):
    for block in blocks:
        block["state"] = "idle"
        block["rect"].topleft = (block["original_x"], block["original_y"])
        block["fall_velocity"] = 0
        block["slide_velocity"] = 0
        block["respawn_protected"] = False
        block["shake_offset"] = 0


# --------------------------------------------------
# Update logic
# --------------------------------------------------

def update_destroblocks(blocks):
    current_time = pygame.time.get_ticks()

    for block in blocks:
        state = block["state"]

        # -------- BREAKING / SHAKE --------
        if state == "breaking":

            # total time since stepped on
            break_elapsed = current_time - block["break_timer"]

            # SHAKE FOR ENTIRE BREAK DURATION
            if break_elapsed < 1500:
                # stronger + visible shake
                block["shake_offset"] = random.randint(-6, 6)
            else:
                block["shake_offset"] = 0

            # transition to falling
            if break_elapsed >= 1500:
                block["state"] = "falling"
                block["fall_velocity"] = 0
                block["slide_velocity"] = random.choice([-2, 2])

        # -------- FALLING --------
        elif state == "falling":
            block["fall_velocity"] += 0.5
            block["rect"].y += block["fall_velocity"]
            block["rect"].x += block["slide_velocity"]
            block["shake_offset"] = 0

            if block["rect"].top > HEIGHT:
                block["state"] = "respawning"
                block["respawn_timer"] = current_time

        # -------- RESPAWNING --------
        elif state == "respawning":
            if current_time - block["respawn_timer"] >= 1000:
                block["rect"].topleft = (
                    block["original_x"],
                    block["original_y"]
                )

                block["state"] = "idle"
                block["fall_velocity"] = 0
                block["slide_velocity"] = 0

                block["respawn_protected"] = True
                block["protect_timer"] = current_time
                block["shake_offset"] = 0

        # -------- PROTECTION --------
        if block["respawn_protected"]:
            if current_time - block["protect_timer"] >= 500:
                block["respawn_protected"] = False