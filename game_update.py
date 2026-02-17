import pygame
from player import (
    handle_movement,
    apply_gravity,
    constrain_to_screen,
    respawn_if_fallen,
    check_block_collision,
    update_jump_state,
)

from blockt import dblocks, sblocks, destroblocks, xblocks


def update_game(
    button_pressed,
    normalblocks,
    specialblocks,   # destroblocks
    hazardblocks,    # xblocks
    platform,
    width,
    height
):
    if button_pressed:
        keys = pygame.key.get_pressed()
        handle_movement(keys)
        apply_gravity()

        # Only solid blocks go into collision
        check_block_collision(
            normalblocks + specialblocks + [{"rect": platform}]
        )

        # Hazard logic
        xblocks.update_xblocks(hazardblocks)

        # Destro logic
        destroblocks.update_destroblocks(specialblocks)

        update_jump_state()

    constrain_to_screen(width)
    respawn_if_fallen(platform, height)

    # Drag logic
    dblocks.update_drag(normalblocks, button_pressed)
    sblocks.update_drag(normalblocks, button_pressed)
    destroblocks.update_drag(specialblocks, button_pressed)
