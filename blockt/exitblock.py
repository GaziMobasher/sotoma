import pygame
import levels
from config import SCALE

# Base (unscaled) reset position
BASE_RESET_X = 350
BASE_RESET_Y = 510

def check_exit_collision(player, exit_rect, current_level):
    # Player rect is already scaled correctly
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    
    if player_rect.colliderect(exit_rect):
        next_level = current_level + 1

        if next_level > levels.TOTAL_LEVELS:
            next_level = 1  # Restart from Level 1 if finished

        platform, rectangles = levels.load_level(next_level)

        # Reset position using SCALE
        player.x = int(BASE_RESET_X * SCALE)
        player.y = int(BASE_RESET_Y * SCALE)

        return next_level, platform, rectangles, False
    
    return current_level, None, None, None
