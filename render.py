# render.py
import pygame
from player import get_current_sprite, update_animation
from blockt import xblocks



def draw_world(
    screen,
    assets,
    platform,
    blocks,
    player,
    exit_rect,
    ui
):
    # Background
    screen.blit(assets["background"], (0, 0))

    # Main platform
    main_img = assets["mainplat"]
    screen.blit(
        main_img,
        (
            platform.x + (platform.width - main_img.get_width()) // 2,
            platform.y + (platform.height - main_img.get_height()) // 2
        )
    )

    # Player
    update_animation()
    sprite = get_current_sprite()
    screen.blit(sprite or assets["player"], player.topleft)
    
    # Drawing bounds on xblock search
    xblock_list = [b for b in blocks if b.get("kind") == "xblock"]
    xblocks.draw_bounds(screen, xblock_list)

    # Blocks
    for block in blocks:
        rect = block["rect"]

        # Default offsets
        offset_x = 0
        offset_y = 0

        # Apply shake ONLY for destro blocks using state system
        if block.get("kind") == "destro":
            offset_x = block.get("shake_offset", 0)

        # -------- BLOCK TYPES --------
        if block["kind"] == "rect":
            screen.blit(assets["subplat"], (rect.x, rect.y))

        elif block["kind"] == "destro":
            screen.blit(
                assets["dplat"],
                (rect.x + offset_x, rect.y + offset_y)
            )

        elif block["kind"] == "sphere":
            splat_img = assets["splat"]
            img_rect = splat_img.get_rect(center=rect.center)
            screen.blit(splat_img, img_rect.topleft)

        elif block["kind"] == "xblock":
            screen.blit(assets["xplat"], (rect.x, rect.y))
        elif block["kind"] == "xblockstat":
            screen.blit(assets["xplat"], (rect.x, rect.y))

        elif block["kind"] == "goo":
            screen.blit(assets["gplat"], (rect.x, rect.y))

    # UI
    screen.blit(assets["start"], (ui["go"].x + 10, ui["go"].y - 5))
    screen.blit(assets["back"], (ui["back"].x + 10, ui["back"].y - 5))
    screen.blit(assets["exit"], (exit_rect.x + 10, exit_rect.y - 5))
    