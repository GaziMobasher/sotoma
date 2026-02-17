import pygame
import os
BASE_WIDTH, BASE_HEIGHT = 800, 600
BG_P = os.path.join("bgs", "utopia.png")
BU_P1 = os.path.join("buttons", "start.png")
BU_P2 = os.path.join("buttons", "back.png")
PL_P1 = os.path.join("platforms", "subplat.png")
PL_P2 = os.path.join("platforms", "mainplat.png")
AV_P = os.path.join("avatar", "sonic.png")
EX_P = os.path.join("exit", "exit.png")
S_P = os.path.join("platforms", "splat.png")
DPL_P = os.path.join("platforms", "dplat.png")
X_P = os.path.join("platforms", "xplat.png")



def load_assets(scale):
    background_img = pygame.image.load(BG_P)
    background_img = pygame.transform.scale(
        background_img,
        (int(BASE_WIDTH * scale), int(BASE_HEIGHT * scale))
    )
    
    player_img = pygame.image.load(AV_P)
    player_img = pygame.transform.scale(
        player_img,
        (int(30 * scale), int(60 * scale))
    )

    subplat_img = pygame.image.load(PL_P1)
    subplat_img = pygame.transform.scale(
        subplat_img,
        (int(170 * scale), int(10 * scale))
    )

    mainplat_img = pygame.image.load(PL_P2)
    mainplat_img = pygame.transform.scale(
        mainplat_img,
        (int(170 * scale), int(30 * scale))
    )

    start_img = pygame.image.load(BU_P1)
    start_img = pygame.transform.scale(
        start_img,
        (int(80 * scale), int(30 * scale))
    )

    back_img = pygame.image.load(BU_P2)
    back_img = pygame.transform.scale(
        back_img,
        (int(80 * scale), int(80 * scale))
    )
    
    exit_img = pygame.image.load(EX_P)
    exit_img = pygame.transform.scale(
        exit_img,
        (int(90 * scale), int(100 * scale))
    )
    splat_img = pygame.image.load(S_P).convert_alpha()
    splat_img = pygame.transform.scale(
        splat_img,
        (int(40 * scale), int(40 * scale))
    )

    dplat_img = pygame.image.load(DPL_P).convert_alpha()
    dplat_img = pygame.transform.scale(
        dplat_img,
        (int(50 * scale), int(50 * scale))  # Adjust height if needed
    )

    xplat_img = pygame.image.load(X_P).convert_alpha()
    xplat_img = pygame.transform.scale(
        xplat_img,
        (int(80 * scale), int(80 * scale))  
    )

    return {
        "background": background_img,
        "player": player_img,
        "subplat": subplat_img,
        "mainplat": mainplat_img,
        "start": start_img,
        "back": back_img,
        "exit": exit_img,
        "splat": splat_img,
        "dplat": dplat_img,
        "xplat": xplat_img
    }

    
def animation_assets(scale):
    NORMAL_W = int(30 * scale)
    NORMAL_H = int(60 * scale)

    DOUBLE_JUMP_SCALE = 1.2 
    DJ_W = int(40 * scale * DOUBLE_JUMP_SCALE)
    DJ_H = int(60 * scale * DOUBLE_JUMP_SCALE)

    JUMP_SCALE = 1
    J_W = int(40 * scale * JUMP_SCALE)
    J_H = int(60 * scale * JUMP_SCALE)

    def load_and_scale_normal(path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (NORMAL_W, NORMAL_H))
    
    def load_and_scale_jump(path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (J_W, J_H))

    def load_and_scale_double_jump(path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (DJ_W, DJ_H))

    return {
        # Player Movement
        "pl1": load_and_scale_normal("left/L (1).png"),
        "pl2": load_and_scale_normal("left/L (2).png"),
        "pl3": load_and_scale_normal("left/L (3).png"),
        "pl4": load_and_scale_normal("left/L (4).png"),
        "pl5": load_and_scale_normal("left/L (5).png"),
        "pl6": load_and_scale_normal("left/L (6).png"),
        
        "pr1": load_and_scale_normal("right/r (1).png"),
        "pr2": load_and_scale_normal("right/r (2).png"),
        "pr3": load_and_scale_normal("right/r (3).png"),
        "pr4": load_and_scale_normal("right/r (4).png"),
        "pr5": load_and_scale_normal("right/r (5).png"),
        "pr6": load_and_scale_normal("right/r (6).png"),

        # Player Jumping (normal size)
        "jl1": load_and_scale_jump("jump_left/Jl1.png"),
        "jl2": load_and_scale_jump("jump_left/Jl2.png"),
        "jl3": load_and_scale_jump("jump_left/Jl3.png"),
        "jl4": load_and_scale_jump("jump_left/Jl4.png"),

        "jr1": load_and_scale_jump("jump_right/J1.png"),
        "jr2": load_and_scale_jump("jump_right/J2.png"),
        "jr3": load_and_scale_jump("jump_right/J3.png"),
        "jr4": load_and_scale_jump("jump_right/J4.png"),

        # Player Double Jumping (slightly larger)
        "djl1": load_and_scale_double_jump("djL/djL (1).png"),
        "djl2": load_and_scale_double_jump("djL/djL (2).png"),
        "djl3": load_and_scale_double_jump("djL/djL (3).png"),
        "djl4": load_and_scale_double_jump("djL/djL (4).png"),
        "djl5": load_and_scale_double_jump("djL/djL (5).png"),
        "djl6": load_and_scale_double_jump("djL/djL (6).png"),

        "djlr": load_and_scale_double_jump("djr/djr (1).png"),
        "djr2": load_and_scale_double_jump("djr/djr (2).png"),
        "djr3": load_and_scale_double_jump("djr/djr (3).png"),
        "djr4": load_and_scale_double_jump("djr/djr (4).png"),
        "djr5": load_and_scale_double_jump("djr/djr (5).png"),
        "djr6": load_and_scale_double_jump("djr/djr (6).png"),
    }
