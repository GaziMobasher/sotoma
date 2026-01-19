import pygame
from assets import load_assets, animation_assets
from player import (
    player,
    handle_movement,
    apply_gravity,
    update_position,
    constrain_to_screen,
    respawn_if_fallen,
    check_platform_collision,
    check_block_collision,
    get_current_sprite,
    load_animation_frames,
    update_animation,
    update_jump_state  
)
from blockt import dblocks
import levels
from blockt import exitblock

pygame.init()

# Screen settings
BASE_WIDTH, BASE_HEIGHT = 800, 600

NEW_WIDTH, NEW_HEIGHT = 1200, 900   # resolution editing

SCALE = NEW_WIDTH / BASE_WIDTH

WIDTH, HEIGHT = NEW_WIDTH, NEW_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Test 1")

# Game settings
clock = pygame.time.Clock()

# Load images, animation frames
assets = load_assets()
anim_assets = animation_assets()
load_animation_frames(anim_assets)

background_img = assets["background"]
player_img = assets["player"]
subplat_img = assets["subplat"]
mainplat_img = assets["mainplat"]
start_img = assets["start"]
back_img = assets["back"]
exit_img = assets["exit"]


# Platform & buttons
go_button_rect = pygame.Rect(WIDTH - 120, 40, 100, 40)
back_button_rect = pygame.Rect(WIDTH - 120, HEIGHT - 60, 100, 40)
exit_rect = pygame.Rect(550, 10, 100, 100)

# Level state
current_level = 1
platform, rectangles = levels.load_level(current_level)

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

            dblocks.handle_mouse_down(rectangles, mouse_x, mouse_y, button_pressed)

        if event.type == pygame.MOUSEBUTTONUP:
            dblocks.handle_mouse_up(rectangles)
    
    if button_pressed:
        keys = pygame.key.get_pressed()
        handle_movement(keys)

    apply_gravity()
    update_position()

    # First resolve collisions (this sets on_ground correctly)
    check_platform_collision(platform)
    check_block_collision(rectangles, button_pressed)

    # Now update jumping state using the UPDATED on_ground
    update_jump_state()

    constrain_to_screen(WIDTH)
    respawn_if_fallen(platform, HEIGHT)

    # Drag logic
    dblocks.update_drag(rectangles, button_pressed)

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
    
    for rect in rectangles:
        screen.blit(subplat_img, (rect["x"], rect["y"]))

    screen.blit(start_img, (go_button_rect.x + 10, go_button_rect.y - 5))

    screen.blit(back_img, (back_button_rect.x + 10, back_button_rect.y - 5))
    
    screen.blit(exit_img, (exit_rect.x + 10, exit_rect.y - 5))
    
    # Check if player touches the exit
    current_level, new_platform, new_rectangles, reset_button = exitblock.check_exit_collision(player, exit_rect, current_level)
    if new_platform is not None:
        platform = new_platform
        rectangles = new_rectangles
        button_pressed = reset_button

    pygame.display.update()
    clock.tick(60)

pygame.quit()
