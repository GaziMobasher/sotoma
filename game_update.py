import pygame
# game_update.py
from player import (
    handle_movement,
    apply_gravity,
    constrain_to_screen,
    respawn_if_fallen,
    check_block_collision,
    update_jump_state
)
from blockt import dblocks, sblocks, destroblocks


def update_game(
    button_pressed,
    blocks,
    platform,
    width,
    height
):
    if button_pressed:
        keys = pygame.key.get_pressed()
        handle_movement(keys)
        apply_gravity()

        check_block_collision(blocks + [{"rect": platform}])

        destroblocks.update_destroblocks(blocks)

        update_jump_state()

    constrain_to_screen(width)
    respawn_if_fallen(platform, height)

    dblocks.update_drag(blocks, button_pressed)
    sblocks.update_drag(blocks, button_pressed)
