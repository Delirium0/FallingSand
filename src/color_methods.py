import random

# Цвета
COLORS = {
    'empty': (0, 0, 0),
    'sand': (194, 178, 128),
    'water': (0, 0, 255),
    'dirt': (140, 122, 70),
    'metal': (128, 128, 128),
}


# рандомизация цвета
def adjust_color(color, variation_range=(-10, 10)):
    return tuple(
        max(0, min(255, c + random.randint(variation_range[0], variation_range[1])))
        for c in color
    )
