import pygame

from assets import load_assets, animation_assets
from player import (
    player,
    load_animation_frames
)

from blockt import destroblocks, exitblock, gblocks
import levels
from config import *
from reset import reset_level

# Modular imports
from render import draw_world
from events import handle_events
from game_update import update_game


# -------------------- INIT --------------------
pygame.init()

WIDTH, HEIGHT = NEW_WIDTH, NEW_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test 1")

clock = pygame.time.Clock()


# -------------------- ASSETS --------------------
assets = load_assets(SCALE)
anim_assets = animation_assets(SCALE)
load_animation_frames(anim_assets)


# -------------------- UI RECTANGLES --------------------
go_button_rect = pygame.Rect(
    WIDTH - int(120 * SCALE),
    int(40 * SCALE),
    int(100 * SCALE),
    int(40 * SCALE)
)

back_button_rect = pygame.Rect(
    WIDTH - int(120 * SCALE),
    HEIGHT - int(100 * SCALE),
    int(100 * SCALE),
    int(100 * SCALE)
)


# -------------------- LEVEL STATE --------------------
current_level = 9
platform, blocks, exit_rect = levels.load_level(current_level)

# Split blocks into separate lists
specialblocks = [b for b in blocks if b.get("kind") == "destro"]
hazardblocks = [b for b in blocks if b.get("kind") == "xblock"]
gooblocks = [b for b in blocks if b.get("kind") == "goo"]
normalblocks = [b for b in blocks if b.get("kind") not in ("destro", "xblock", "goo")]


# -------------------- GAME STATE --------------------
button_pressed = False
running = True


# ==================== GAME LOOP ====================
while running:

    # -------- EVENTS --------
    running, button_pressed, reset_data = handle_events(
        normalblocks=normalblocks,
        specialblocks=specialblocks,
        hazardblocks=hazardblocks,
        gooblocks=gooblocks,
        go_button=go_button_rect,
        back_button=back_button_rect,
        reset_fn=reset_level,
        current_level=current_level,
        button_pressed=button_pressed
    )

    if not running:
        break

    if reset_data:
        platform, blocks, exit_rect = reset_data

        # Re-split after reset
        specialblocks = [b for b in blocks if b.get("kind") == "destro"]
        hazardblocks = [b for b in blocks if b.get("kind") == "xblock"]
        normalblocks = [b for b in blocks if b.get("kind") not in ("destro", "xblock")]
        gooblocks = [b for b in blocks if b.get("kind") == "goo"]


    # -------- UPDATE --------
    update_game(
        button_pressed=button_pressed,
        normalblocks=normalblocks,
        specialblocks=specialblocks,
        hazardblocks=hazardblocks,
        gooblocks=gooblocks,
        platform=platform,
        width=WIDTH,
        height=HEIGHT
    )


    # -------- LEVEL EXIT CHECK --------
    current_level, new_platform, new_blocks, new_exit_rect, reset_button = \
        exitblock.check_exit_collision(player, exit_rect, current_level)

    if new_platform is not None:
        platform = new_platform
        blocks = new_blocks
        exit_rect = new_exit_rect
        button_pressed = False

        #Re-split after level change
        specialblocks = [b for b in blocks if b.get("kind") == "destro"]
        hazardblocks = [b for b in blocks if b.get("kind") == "xblock"]
        normalblocks = [b for b in blocks if b.get("kind") not in ("destro", "xblock")]
        gooblocks = [b for b in blocks if b.get("kind") == "goo"]


    # -------- DRAW --------
    draw_world(
        screen=screen,
        assets=assets,
        platform=platform,
        blocks=normalblocks + specialblocks + hazardblocks + gooblocks,
        player=player,
        exit_rect=exit_rect,
        ui={
            "go": go_button_rect,
            "back": back_button_rect
        }
    )

    pygame.display.update()
    clock.tick(60)

pygame.quit()
