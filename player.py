import pygame
from config import SCALE

# Animation settings
LEFT_FRAMES = []
RIGHT_FRAMES = []
JUMP_LEFT_FRAMES = []
JUMP_RIGHT_FRAMES = []
DOUBLE_JUMP_LEFT_FRAMES = []
DOUBLE_JUMP_RIGHT_FRAMES = []
frame_index = 0
animation_timer = 0
ANIMATION_DELAY = 5  # Controls animation speed (lower is faster)
JUMP_ANIMATION_DELAY = 12 # Controls jump animation speed
DOUBLE_JUMP_ANIMATION_DELAY = 6 # Controls double jump animation speed


def load_animation_frames(assets):
    global LEFT_FRAMES, RIGHT_FRAMES
    global JUMP_LEFT_FRAMES, JUMP_RIGHT_FRAMES
    global DOUBLE_JUMP_LEFT_FRAMES, DOUBLE_JUMP_RIGHT_FRAMES

    LEFT_FRAMES = [
        assets["pl1"], assets["pl2"], assets["pl3"],
        assets["pl4"], assets["pl5"], assets["pl6"]
    ]

    RIGHT_FRAMES = [
        assets["pr1"], assets["pr2"], assets["pr3"],
        assets["pr4"], assets["pr5"], assets["pr6"]
    ]

    # First jump
    JUMP_LEFT_FRAMES = [
        assets["jl1"], assets["jl2"], assets["jl3"], assets["jl4"]
    ]
    JUMP_RIGHT_FRAMES = [
        assets["jr1"], assets["jr2"], assets["jr3"], assets["jr4"]
    ]

    # Double jump
    DOUBLE_JUMP_LEFT_FRAMES = [
        assets["djl1"], assets["djl2"], assets["djl3"],
        assets["djl4"], assets["djl5"], assets["djl6"]
    ]

    DOUBLE_JUMP_RIGHT_FRAMES = [
        assets["djlr"], assets["djr2"], assets["djr3"],
        assets["djr4"], assets["djr5"], assets["djr6"]
    ]
    

# Player settings
PLAYER_WIDTH = int(30 * SCALE)
PLAYER_HEIGHT = int(60 * SCALE)
PLAYER_START_X = int(350 * SCALE)
PLAYER_START_Y = int((600 - 90) * SCALE)


# Movement settings
PLAYER_SPEED = 7
JUMP_STRENGTH = -10
GRAVITY = 0.5

# Initialize player rectangle
player = pygame.Rect(PLAYER_START_X, PLAYER_START_Y, PLAYER_WIDTH, PLAYER_HEIGHT)

# Initialize player state
player_velocity_x = 0
player_velocity_y = 0
facing_left = False
facing_right = False

on_ground = False

dj = 0  # Double jump counter
jump_pressed = False
jumping = False
double_jumping = False
jumped_from_ground = False

# Helper code for jumps and double jumps
def reset_animation():
    global frame_index, animation_timer
    frame_index = 0
    animation_timer = 0

def handle_movement(keys):
    global player_velocity_x, player_velocity_y, jump_pressed, dj, on_ground
    global facing_left, facing_right, jumping, double_jumping, jumped_from_ground
    player_velocity_x = 0
    facing_left = False
    facing_right = False
    
    if keys[pygame.K_a]:
        player_velocity_x = -PLAYER_SPEED
        facing_left = True
    if keys[pygame.K_d]:
        player_velocity_x = PLAYER_SPEED
        facing_right = True

    if keys[pygame.K_w] or keys[pygame.K_SPACE]:
        if not jump_pressed:

            # FIRST JUMP
            if dj == 0:
                player_velocity_y = JUMP_STRENGTH
                dj = 1

                if on_ground:
                    # Jump started from ground = normal jump animation, double jump later allowed
                    jumped_from_ground = True
                    double_jumping = False

                else:
                    # Jump started from falling = THIS is the double jump animation
                    jumped_from_ground = False      # no second jump allowed later
                    double_jumping = True          

                reset_animation()

            # SECOND JUMP (double jump) — ONLY if first jump was from ground
            elif dj == 1 and jumped_from_ground:
                player_velocity_y = JUMP_STRENGTH
                dj = 2
                double_jumping = True               # second jump animation
                reset_animation()

            # Else: no more jumps allowed

            jump_pressed = True
            jumping = True
    else:
        jump_pressed = False
        
    # if on_ground:
    #     jumping = False

def apply_gravity():
    global player_velocity_y
    player_velocity_y += GRAVITY

def update_position():
    global player
    player.x += player_velocity_x
    player.y += player_velocity_y

# New global jumping code added here
def update_jump_state():
    global jumping, double_jumping, jumped_from_ground, frame_index, dj

    was_jumping = jumping
    jumping = not on_ground

    # If just landed
    if was_jumping and not jumping:
        frame_index = 0
        double_jumping = False
        jumped_from_ground = False   #reset
        dj = 0

def constrain_to_screen(width):
    global player
    if player.x < 0:
        player.x = 0
    if player.x + player.width > width:
        player.x = width - player.width

def respawn_if_fallen(platform, height):
    global player, player_velocity_y, on_ground, dj
    if player.y > height:
        player.x = platform.x + platform.width // 2 - player.width // 2
        player.y = platform.y - player.height
        player_velocity_y = 0
        on_ground = True
        dj = 0

def check_platform_collision(platform):
    global player, player_velocity_y, on_ground, dj
    on_ground = False
    if player.colliderect(platform):
        player.y = platform.y - player.height
        player_velocity_y = 0
        on_ground = True
        dj = 0

def check_block_collision(blocks):
    global player, player_velocity_x, player_velocity_y, on_ground, dj

    # -------- HORIZONTAL COLLISION --------
    player.x += player_velocity_x
    for rect in blocks:
        block = rect["rect"] if "rect" in rect else pygame.Rect(
            rect["x"],
            rect["y"],
            int(170 * SCALE),
            int(10 * SCALE)
        )
        if player.colliderect(block):
            if player_velocity_x > 0:
                player.right = block.left
            elif player_velocity_x < 0:
                player.left = block.right

    # -------- VERTICAL COLLISION --------
    player.y += player_velocity_y
    on_ground = False

    for rect in blocks:
        block = rect["rect"] if "rect" in rect else pygame.Rect(
            rect["x"],
            rect["y"],
            int(170 * SCALE),
            int(10 * SCALE)
        )
        if player.colliderect(block):
            if player_velocity_y > 0:  # landing
                player.bottom = block.top
                player_velocity_y = 0
                on_ground = True
                dj = 0
            elif player_velocity_y < 0:  # hitting head
                player.top = block.bottom
                player_velocity_y = 0


def get_current_sprite():
    global frame_index

    # Double jump has priority
    if jumping and double_jumping:
        frames = DOUBLE_JUMP_LEFT_FRAMES if facing_left else DOUBLE_JUMP_RIGHT_FRAMES
    elif jumping:
        frames = JUMP_LEFT_FRAMES if facing_left else JUMP_RIGHT_FRAMES
    elif facing_left:
        frames = LEFT_FRAMES
    elif facing_right:
        frames = RIGHT_FRAMES
    else:
        return None

    if not frames:
        return None

    # possibility of indexerror safe fix
    if frame_index >= len(frames):
        frame_index = len(frames) - 1

    return frames[frame_index]



def update_animation():
    global frame_index, animation_timer, jumping, double_jumping

    animation_timer += 1

    # Choose active frames and delay
    if jumping and double_jumping:
        active_frames = DOUBLE_JUMP_LEFT_FRAMES if facing_left else DOUBLE_JUMP_RIGHT_FRAMES
        delay = DOUBLE_JUMP_ANIMATION_DELAY
    elif jumping:
        active_frames = JUMP_LEFT_FRAMES if facing_left else JUMP_RIGHT_FRAMES
        delay = JUMP_ANIMATION_DELAY
    elif facing_left:
        active_frames = LEFT_FRAMES
        delay = ANIMATION_DELAY
    elif facing_right:
        active_frames = RIGHT_FRAMES
        delay = ANIMATION_DELAY
    else:
        active_frames = []
        delay = ANIMATION_DELAY

    if not active_frames:
        frame_index = 0
        return

    if animation_timer >= delay:
        animation_timer = 0

        if jumping:
            # NON-LOOPING for both jump and double jump
            if frame_index < len(active_frames) - 1:
                frame_index += 1
            else:
                frame_index = len(active_frames) - 1
        else:
            # Looping walk
            frame_index = (frame_index + 1) % len(active_frames)
