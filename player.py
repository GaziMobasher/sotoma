import pygame
from config import SCALE

# -------------------- ANIMATION SETTINGS --------------------
LEFT_FRAMES = []
RIGHT_FRAMES = []
JUMP_LEFT_FRAMES = []
JUMP_RIGHT_FRAMES = []
DOUBLE_JUMP_LEFT_FRAMES = []
DOUBLE_JUMP_RIGHT_FRAMES = []
frame_index = 0
animation_timer = 0
ANIMATION_DELAY = 5
JUMP_ANIMATION_DELAY = 12
DOUBLE_JUMP_ANIMATION_DELAY = 6

# -------------------- PLAYER SETTINGS --------------------
PLAYER_WIDTH = int(30 * SCALE)
PLAYER_HEIGHT = int(60 * SCALE)
PLAYER_START_X = int(350 * SCALE)
PLAYER_START_Y = int((600 - 90) * SCALE)

PLAYER_SPEED = 7
JUMP_STRENGTH = -11
GRAVITY = 0.5
FRICTION = 1.0

player = pygame.Rect(PLAYER_START_X, PLAYER_START_Y, PLAYER_WIDTH, PLAYER_HEIGHT)

player_velocity_x = 0
player_velocity_y = 0
facing_left = False
facing_right = False
on_ground = False
dj = 0
jump_pressed = False
jumping = False
double_jumping = False
jumped_from_ground = False

# -------------------- ASSET LOADING --------------------
def load_animation_frames(assets):
    global LEFT_FRAMES, RIGHT_FRAMES
    global JUMP_LEFT_FRAMES, JUMP_RIGHT_FRAMES
    global DOUBLE_JUMP_LEFT_FRAMES, DOUBLE_JUMP_RIGHT_FRAMES

    LEFT_FRAMES = [assets["pl1"], assets["pl2"], assets["pl3"],
                   assets["pl4"], assets["pl5"], assets["pl6"]]
    RIGHT_FRAMES = [assets["pr1"], assets["pr2"], assets["pr3"],
                    assets["pr4"], assets["pr5"], assets["pr6"]]
    JUMP_LEFT_FRAMES = [assets["jl1"], assets["jl2"], assets["jl3"], assets["jl4"]]
    JUMP_RIGHT_FRAMES = [assets["jr1"], assets["jr2"], assets["jr3"], assets["jr4"]]
    DOUBLE_JUMP_LEFT_FRAMES = [assets["djl1"], assets["djl2"], assets["djl3"],
                               assets["djl4"], assets["djl5"], assets["djl6"]]
    DOUBLE_JUMP_RIGHT_FRAMES = [assets["djlr"], assets["djr2"], assets["djr3"],
                                assets["djr4"], assets["djr5"], assets["djr6"]]

# -------------------- MOVEMENT --------------------
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
        player_velocity_x = -PLAYER_SPEED * FRICTION
        facing_left = True
    if keys[pygame.K_d]:
        player_velocity_x = PLAYER_SPEED * FRICTION
        facing_right = True

    if keys[pygame.K_w] or keys[pygame.K_SPACE]:
        if not jump_pressed:
            if dj == 0:
                player_velocity_y = JUMP_STRENGTH * FRICTION
                dj = 1
                if on_ground:
                    jumped_from_ground = True
                    double_jumping = False
                else:
                    jumped_from_ground = False
                    double_jumping = True
                reset_animation()
            elif dj == 1 and jumped_from_ground:
                player_velocity_y = JUMP_STRENGTH * FRICTION
                dj = 2
                double_jumping = True
                reset_animation()
            jump_pressed = True
            jumping = True
    else:
        jump_pressed = False

def apply_gravity():
    global player_velocity_y
    player_velocity_y += GRAVITY

def update_position():
    global player
    player.x += player_velocity_x
    player.y += player_velocity_y

def update_jump_state():
    global jumping, double_jumping, jumped_from_ground, frame_index, dj
    was_jumping = jumping
    jumping = not on_ground
    if was_jumping and not jumping:
        frame_index = 0
        double_jumping = False
        jumped_from_ground = False
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

# -------------------- COLLISION --------------------
def check_block_collision(blocks):
    global player, player_velocity_x, player_velocity_y, on_ground, dj, FRICTION
    FRICTION = 1.0

    # Horizontal movement
    player.x += player_velocity_x
    for block in blocks:
        if block.get("kind") == "xblock":
            continue
        if block.get("state") in ("falling", "respawning"):
            continue
        if player.colliderect(block["rect"]):
            if player_velocity_x > 0:
                player.right = block["rect"].left
            elif player_velocity_x < 0:
                player.left = block["rect"].right

    # Vertical movement
    player.y += player_velocity_y
    on_ground = False
    for block in blocks:
        if block.get("kind") == "xblock":
            continue
        if block.get("state") in ("falling", "respawning"):
            continue

        rect = block["rect"]
        if not player.colliderect(rect):
            continue

        # Landing
        if player_velocity_y > 0:
            player.bottom = rect.top
            player_velocity_y = 0
            on_ground = True
            dj = 0
            if block.get("kind") == "destro" and block["state"] == "idle":
                block["state"] = "breaking"
                block["break_timer"] = pygame.time.get_ticks()
            if block.get("kind") == "sphere":
                radius = rect.width // 2
                sphere_center_x = rect.centerx
                player_center_x = player.centerx
                offset = (player_center_x - sphere_center_x) / radius
                offset = max(-1, min(1, offset))
                SLIP_STRENGTH = 3.2
                player_velocity_x += offset * SLIP_STRENGTH

        # Head hit
        elif player_velocity_y < 0:
            player.top = rect.bottom
            player_velocity_y = 0

    # Friction
    if on_ground:
        for block in blocks:
            if block.get("kind") == "goo":
                rect = block["rect"]
                if player.bottom == rect.top and player.right > rect.left and player.left < rect.right:
                    FRICTION = 0.4
                    break

# -------------------- ANIMATION --------------------
def get_current_sprite():
    global frame_index
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
    if frame_index >= len(frames):
        frame_index = len(frames) - 1
    return frames[frame_index]

def update_animation():
    global frame_index, animation_timer, jumping, double_jumping
    animation_timer += 1
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
            frame_index = min(frame_index + 1, len(active_frames) - 1)
        else:
            frame_index = (frame_index + 1) % len(active_frames)

def reset_full_player_state():
    global frame_index, animation_timer
    global player_velocity_x, player_velocity_y
    global facing_left, facing_right
    global jumping, double_jumping, jumped_from_ground
    global on_ground, dj, jump_pressed

    player_velocity_x = 0
    player_velocity_y = 0
    frame_index = 0
    animation_timer = 0
    facing_left = False
    facing_right = False
    jumping = False
    double_jumping = False
    jumped_from_ground = False
    on_ground = False
    dj = 0
    jump_pressed = False