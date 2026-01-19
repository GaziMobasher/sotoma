import pygame
import os

WIDTH, HEIGHT = 800, 600
BG_P = os.path.join("bgs", "utopia.png")
BU_P1 = os.path.join("buttons", "start.png")
BU_P2 = os.path.join("buttons", "back.png")
PL_P1 = os.path.join("platforms", "subplat.png")
PL_P2 = os.path.join("platforms", "mainplat.png")
AV_P = os.path.join("avatar", "sonic.png")
EX_P = os.path.join("exit", "exit.png")

def load_assets(scale):
    background_img = pygame.image.load(BG_P)
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    
    player_img = pygame.image.load(AV_P)
    player_img = pygame.transform.scale(player_img, (30, 60))

    subplat_img = pygame.image.load(PL_P1)
    subplat_img = pygame.transform.scale(subplat_img, (170, 10))

    mainplat_img = pygame.image.load(PL_P2)
    mainplat_img = pygame.transform.scale(mainplat_img, (200, 30))

    start_img = pygame.image.load(BU_P1)
    start_img = pygame.transform.scale(start_img, (80, 30))

    back_img = pygame.image.load(BU_P2)
    back_img = pygame.transform.scale(back_img, (80, 30))
    
    exit_img = pygame.image.load(EX_P)
    exit_img = pygame.transform.scale(exit_img, (80, 100))

    return {
        "background": background_img,
        "player": player_img,
        "subplat": subplat_img,
        "mainplat": mainplat_img,
        "start": start_img,
        "back": back_img,
        "exit": exit_img
    }
    
def animation_assets(scale):
    def load_and_scale(path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (30, 60))
    
    return {
        "pl1": load_and_scale("left/L (1).png"),
        "pl2": load_and_scale("left/L (2).png"),
        "pl3": load_and_scale("left/L (3).png"),
        "pl4": load_and_scale("left/L (4).png"),
        "pl5": load_and_scale("left/L (5).png"),
        "pl6": load_and_scale("left/L (6).png"),
        
        "pr1": load_and_scale("right/r (1).png"),
        "pr2": load_and_scale("right/r (2).png"),
        "pr3": load_and_scale("right/r (3).png"),
        "pr4": load_and_scale("right/r (4).png"),
        "pr5": load_and_scale("right/r (5).png"),
        "pr6": load_and_scale("right/r (6).png"),
        
        "jl1": load_and_scale("jump_left/Jl1.png"),
        "jl2": load_and_scale("jump_left/Jl2.png"),
        "jl3": load_and_scale("jump_left/Jl3.png"),
        "jl4": load_and_scale("jump_left/Jl4.png"),

        "jr1": load_and_scale("jump_right/J1.png"),
        "jr2": load_and_scale("jump_right/J2.png"),
        "jr3": load_and_scale("jump_right/J3.png"),
        "jr4": load_and_scale("jump_right/J4.png"),
    }