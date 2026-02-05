# reset.py
from player import (
    player,
    PLAYER_START_X,
    PLAYER_START_Y,
    reset_animation
)
import levels


def reset_level(level_number):
    """
    Fully reset the current level:
    - reload platform & blocks
    - reset player position and animation
    """
    # Reload level data
    platform, rectangles = levels.load_level(level_number)

    # Reset player position
    player.x = PLAYER_START_X
    player.y = PLAYER_START_Y

    # Reset animation
    reset_animation()

    # Reset player physics safely
    from player import (
        player_velocity_x,
        player_velocity_y,
        on_ground,
        dj,
        jumping,
        double_jumping,
        jumped_from_ground
    )

    player_velocity_x = 0
    player_velocity_y = 0
    on_ground = False
    dj = 0
    jumping = False
    double_jumping = False
    jumped_from_ground = False

    return platform, rectangles
