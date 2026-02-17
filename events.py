import pygame
from blockt import dblocks, sblocks, destroblocks

def handle_events(
    normalblocks,
    specialblocks,
    hazardblocks,
    go_button,
    back_button,
    reset_fn,
    current_level,
    button_pressed
):
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            return False, button_pressed, None

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if go_button.collidepoint(mx, my):
                button_pressed = True

            elif back_button.collidepoint(mx, my):
                button_pressed = False
                return True, button_pressed, reset_fn(current_level)

            # Drag only normal + special
            dblocks.handle_mouse_down(normalblocks, mx, my, button_pressed)
            sblocks.handle_mouse_down(normalblocks, mx, my, button_pressed)
            destroblocks.handle_mouse_down(specialblocks, mx, my, button_pressed)

        if event.type == pygame.MOUSEBUTTONUP:
            dblocks.handle_mouse_up(normalblocks)
            sblocks.handle_mouse_up(normalblocks)
            destroblocks.handle_mouse_up(specialblocks)

    return True, button_pressed, None
