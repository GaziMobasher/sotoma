import importlib
import pygame

TOTAL_LEVELS = 10  # Set your total number of levels

def load_level(level_number):
    try:
        module = importlib.import_module(f"levelb.level{level_number}")
        return module.load()
    except (ModuleNotFoundError, AttributeError):
        print(f"Level {level_number} not found.")
        return pygame.Rect(0, 0, 0, 0), []
