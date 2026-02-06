import pygame
import levels
from config import SCALE
from reset import reset_full_player_state


# Base (unscaled) reset position
BASE_RESET_X = 350
BASE_RESET_Y = 510

def check_exit_collision(player, exit_rect, current_level):
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)

    # --- SHRINK EXIT COLLISION ZONE ---
    shrink_x = int(40 * SCALE)   # horizontal shrink (left + right)
    shrink_y = int(50 * SCALE)   # vertical shrink (top + bottom)

    exit_trigger = exit_rect.inflate(-shrink_x, -shrink_y)

    if player_rect.colliderect(exit_trigger):
        next_level = current_level + 1

        if next_level > levels.TOTAL_LEVELS:
            next_level = 1
    
        platform, rectangles, exit_rect = levels.load_level(next_level)

        # Reset position
        player.x = int(BASE_RESET_X * SCALE)
        player.y = int(BASE_RESET_Y * SCALE)
        reset_full_player_state()

        return next_level, platform, rectangles, exit_rect, False


    return current_level, None, None, None, None
