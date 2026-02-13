# render.py
import pygame
from player import get_current_sprite, update_animation
import random

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

    # Blocks
    for block in blocks:
        if block["kind"] == "rect":
            screen.blit(assets["subplat"], block["rect"].topleft)
        
        elif block["kind"] == "destro":
            if block.get("breaking"):
                shake_x = random.randint(-2, 2)
                shake_y = random.randint(-2, 2)
                screen.blit(assets["dplat"], (block["rect"].x + shake_x, block["rect"].y + shake_y))
            else:
                screen.blit(assets["dplat"], block["rect"].topleft)

            
        elif block["kind"] == "sphere":
            splat_img = assets["splat"]

            img_rect = splat_img.get_rect(
                center=block["rect"].center
            )

            screen.blit(splat_img, img_rect.topleft)
        


    # UI
    screen.blit(assets["start"], (ui["go"].x + 10, ui["go"].y - 5))
    screen.blit(assets["back"], (ui["back"].x + 10, ui["back"].y - 5))
    screen.blit(assets["exit"], (exit_rect.x + 10, exit_rect.y - 5))
