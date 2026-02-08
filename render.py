# render.py
import pygame
from player import get_current_sprite, update_animation

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
        elif block["kind"] == "sphere":
            screen.blit(assets["splat"], block["rect"].topleft)

    # UI
    screen.blit(assets["start"], (ui["go"].x + 10, ui["go"].y - 5))
    screen.blit(assets["back"], (ui["back"].x + 10, ui["back"].y - 5))
    screen.blit(assets["exit"], (exit_rect.x + 10, exit_rect.y - 5))
