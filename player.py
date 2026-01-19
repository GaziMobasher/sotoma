import pygame

# Animation settings
LEFT_FRAMES = []
RIGHT_FRAMES = []
JUMP_LEFT_FRAMES = []
JUMP_RIGHT_FRAMES = []
frame_index = 0
animation_timer = 0
ANIMATION_DELAY = 5  # Controls animation speed (lower is faster)
JUMP_ANIMATION_DELAY = 10 # Controls jump animation speed

def load_animation_frames(assets):
    global LEFT_FRAMES
    global RIGHT_FRAMES
    global JUMP_LEFT_FRAMES
    global JUMP_RIGHT_FRAMES
    LEFT_FRAMES = [
        assets["pl1"],
        assets["pl2"],
        assets["pl3"],
        assets["pl4"],
        assets["pl5"],
        assets["pl6"]
    ]
    RIGHT_FRAMES = [
        assets["pr1"],
        assets["pr2"],
        assets["pr3"],
        assets["pr4"],
        assets["pr5"],
        assets["pr6"]
    ]
    JUMP_RIGHT_FRAMES = [
        assets["jr1"],
        assets["jr2"],
        assets["jr3"],
        assets["jr4"]
    ]
    JUMP_LEFT_FRAMES = [
        assets["jl1"],
        assets["jl2"],
        assets["jl3"],
        assets["jl4"]
    ]
    

# Player settings
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 60
PLAYER_START_X = 350
PLAYER_START_Y = 600 - 90  # HEIGHT - 90

# Movement settings
PLAYER_SPEED = 5
JUMP_STRENGTH = -10
GRAVITY = 0.5

# Initialize player rectangle
player = pygame.Rect(PLAYER_START_X, PLAYER_START_Y, PLAYER_WIDTH, PLAYER_HEIGHT)

# Initialize player state
player_velocity_x = 0
player_velocity_y = 0
on_ground = False
dj = 0  # Double jump counter
jump_pressed = False
jumping = False
facing_left = False
facing_right = False

def handle_movement(keys):
    global player_velocity_x, player_velocity_y, jump_pressed, dj, on_ground, facing_left, facing_right, jumping
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
            if on_ground:
                player_velocity_y = JUMP_STRENGTH
                dj = 1
            elif dj < 2:
                player_velocity_y = JUMP_STRENGTH
                dj += 1
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
    global jumping
    jumping = not on_ground

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

def check_block_collision(blocks, button_pressed):
    global player, player_velocity_x, player_velocity_y, on_ground, dj
    for rect in blocks:
        block = rect["rect"] if "rect" in rect else pygame.Rect(rect["x"], rect["y"], 170, 10)
        if button_pressed and player.colliderect(block) and player_velocity_y > 0 and player.bottom >= block.top:
            player.y = block.y - player.height
            player_velocity_y = 0
            on_ground = True
            dj = 0

        if player.colliderect(block):
            if player_velocity_x > 0:
                player.x = block.left - player.width
            elif player_velocity_x < 0:
                player.x = block.right

def get_current_sprite():
    if jumping:
        if facing_left and JUMP_LEFT_FRAMES:
            return JUMP_LEFT_FRAMES[frame_index % len(JUMP_LEFT_FRAMES)]
        elif facing_right and JUMP_RIGHT_FRAMES:
            return JUMP_RIGHT_FRAMES[frame_index % len(JUMP_RIGHT_FRAMES)]


    if facing_left and LEFT_FRAMES:
        return LEFT_FRAMES[frame_index]
    elif facing_right and RIGHT_FRAMES:
        return RIGHT_FRAMES[frame_index]
    return None

def update_animation():
    global frame_index, animation_timer, jumping

    animation_timer += 1

    # Choose active frames and delay
    if jumping:
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

    # Update frame only when timer reaches delay
    if animation_timer >= delay:
        animation_timer = 0

        if jumping:
            # NON-LOOPING jump animation
            if frame_index < len(active_frames) - 1:
                frame_index += 1
            else:
                # Stay on last jump frame
                frame_index = len(active_frames) - 1
        else:
            # Normal looping walk animation
            frame_index = (frame_index + 1) % len(active_frames)