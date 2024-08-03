from src.default.materials import Material, Solid, MoveSolid, Liquid
from src.color_methods import adjust_color, COLORS


class Sand(MoveSolid):
    def __init__(self, x, y):
        super().__init__('sand', adjust_color(COLORS['sand']), x, y)


class Metal(Solid):
    def __init__(self, x, y):
        super().__init__('metal', adjust_color(COLORS['metal']), x, y)


class Water(Liquid):
    def __init__(self, x, y):
        super().__init__('water', adjust_color(COLORS['water']), x, y)
