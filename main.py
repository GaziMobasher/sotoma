import pygame
from assets import load_assets, animation_assets
from player import (
    player,
    handle_movement,
    apply_gravity,
    constrain_to_screen,
    respawn_if_fallen,
    check_block_collision,
    get_current_sprite,
    load_animation_frames,
    update_animation,
    update_jump_state  
)
from blockt import dblocks, exitblock, sblocks
import levels
from config import *
from reset import reset_level



pygame.init()
# Screen settings

WIDTH, HEIGHT = NEW_WIDTH, NEW_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Test 1")

# Game settings
clock = pygame.time.Clock()

# Load images, animation frames
assets = load_assets(SCALE)
anim_assets = animation_assets(SCALE)
load_animation_frames(anim_assets)

background_img = assets["background"]
player_img = assets["player"]
subplat_img = assets["subplat"]
mainplat_img = assets["mainplat"]
splat_img = assets["splat"]
start_img = assets["start"]
back_img = assets["back"]
exit_img = assets["exit"]


# Platform & buttons
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

# Level state
current_level = 3
platform, blocks, exit_rect = levels.load_level(current_level)

# Game state
button_pressed = False
running = True

# Game loop
while running:
    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if go_button_rect.collidepoint(mouse_x, mouse_y):
                button_pressed = True
            elif back_button_rect.collidepoint(mouse_x, mouse_y):
                button_pressed = False
                platform, blocks, exit_rect = reset_level(current_level)

            dblocks.handle_mouse_down(blocks, mouse_x, mouse_y, button_pressed)
            sblocks.handle_mouse_down(blocks, mouse_x, mouse_y, button_pressed)


        if event.type == pygame.MOUSEBUTTONUP:
            dblocks.handle_mouse_up(blocks)
            sblocks.handle_mouse_up(blocks)
    
    if button_pressed:
        keys = pygame.key.get_pressed()
        handle_movement(keys)
        
        apply_gravity()

        check_block_collision(blocks + [{"rect": platform}])

        update_jump_state()


    constrain_to_screen(WIDTH)
    respawn_if_fallen(platform, HEIGHT)

    # Drag logic
    dblocks.update_drag(blocks, button_pressed)
    sblocks.update_drag(blocks, button_pressed)

    # Draw everything
    screen.blit(mainplat_img, (platform.x + (platform.width - mainplat_img.get_width()) // 2,
                               platform.y + (platform.height - mainplat_img.get_height()) // 2))
    # screen.blit(player_img, (player.x, player.y))
    update_animation()

    current_sprite = get_current_sprite()
    if current_sprite:
        screen.blit(current_sprite, (player.x, player.y))
    else:
        screen.blit(player_img, (player.x, player.y))
    
    for block in blocks:
        if block["kind"] == "rect":
            screen.blit(subplat_img, block["rect"].topleft)
        elif block["kind"] == "sphere":
            screen.blit(splat_img, block["rect"].topleft)
            

    screen.blit(start_img, (go_button_rect.x + 10, go_button_rect.y - 5))

    screen.blit(back_img, (back_button_rect.x + 10, back_button_rect.y - 5))
    
    screen.blit(exit_img, (exit_rect.x + 10, exit_rect.y - 5))
    
    # Check if player touches the exit
    current_level, new_platform, new_blocks, new_exit_rect, reset_button = \
    exitblock.check_exit_collision(player, exit_rect, current_level)

    if new_platform is not None:
        platform = new_platform
        blocks = new_blocks
        exit_rect = new_exit_rect
        button_pressed = False



    pygame.display.update()
    clock.tick(60)

pygame.quit()
