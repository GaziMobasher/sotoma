from player import (
    player,
    PLAYER_START_X,
    PLAYER_START_Y,
    reset_full_player_state,
)
import levels


reset_full_player_state()


def reset_level(level_number):
    platform, rectangles = levels.load_level(level_number)

    player.x = PLAYER_START_X
    player.y = PLAYER_START_Y

    reset_full_player_state()

    return platform, rectangles
