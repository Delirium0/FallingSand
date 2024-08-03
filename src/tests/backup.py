import pygame
import random

# Настройки экрана
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 4

# Цвета
COLORS = {
    'empty': (0, 0, 0),
    'sand': (194, 178, 128),
    'water': (0, 0, 255),
    'dirt': (140, 122, 70),
    'metal': (128, 128, 128),
}

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("qefqefqef Sand qefqefqefqe")
font = pygame.font.Font(None, 36)

# Создание сетки
grid_width = WIDTH // CELL_SIZE
grid_height = HEIGHT // CELL_SIZE
grid = [[None for _ in range(grid_height)] for _ in range(grid_width)]


class Material:
    def __init__(self, name, color, condition, dispersion_rate=1):
        self.name = name
        self.color = color
        self.condition = condition
        self.dispersion_rate = dispersion_rate

    def update(self, x, y, grid):
        pass


class Solid(Material):
    def __init__(self, name, color):
        super().__init__(name, color, 'Solid')


class MoveSolid(Solid):
    def __init__(self, name, color):
        super().__init__(name, color)

    def update(self, x, y, grid):
        if y + 1 < grid_height:
            target_cell = grid[x][y + 1]
            if target_cell is None:
                grid[x][y], grid[x][y + 1] = None, self

            elif isinstance(target_cell, Liquid):
                grid[x][y], grid[x][y + 1] = target_cell, self

            elif isinstance(target_cell, Solid):
                if y + 1 < grid_height and x > 0 and grid[x - 1][y + 1] is None:
                    grid[x][y], grid[x - 1][y + 1] = None, self
                elif y + 1 < grid_height and x < grid_width - 1 and grid[x + 1][y + 1] is None:
                    grid[x][y], grid[x + 1][y + 1] = None, self


class Liquid(Material):
    def __init__(self, name, color):
        self.dispersion_rape = 5
        super().__init__(name, color, 'Liquid', self.dispersion_rape)

    def update(self, x, y, grid):
        if y + 1 < len(grid[0]) and grid[x][y + 1] is None:
            grid[x][y], grid[x][y + 1] = None, self
        elif y + 1 < len(grid[0]) and x > 0 and grid[x - 1][y + 1] is None:
            grid[x][y], grid[x - 1][y + 1] = None, self
        elif y + 1 < len(grid[0]) and x < len(grid) - 1 and grid[x + 1][y + 1] is None:
            grid[x][y], grid[x + 1][y + 1] = None, self
        else:
            direction = random.choice([-1, 1])
            if direction == -1:
                for dispersion_range in range(1, self.dispersion_rape):
                    if 0 <= x - dispersion_range < len(grid) and grid[x - dispersion_range][y] is None:
                        grid[x - dispersion_range][y], grid[x - dispersion_range + 1][y] = self, None
                    else:
                        break
            else:
                for dispersion_range in range(1, self.dispersion_rape):
                    if 0 <= x + dispersion_range < len(grid) and grid[x + dispersion_range][y] is None:
                        grid[x + dispersion_range][y], grid[x + dispersion_range - 1][y] = self, None
                    else:
                        break


class Sand(MoveSolid):
    def __init__(self):
        super().__init__('sand', COLORS['sand'])


class Metal(Solid):
    def __init__(self):
        super().__init__('metal', COLORS['metal'])


class Water(Liquid):
    def __init__(self):
        super().__init__('water', COLORS['water'], )


def draw_grid():
    for x in range(grid_width):
        for y in range(grid_height):
            material = grid[x][y]
            color = material.color if material else COLORS['empty']
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def update_grid():
    for y in range(grid_height - 1, -1, -1):
        for x in range(grid_width):
            material = grid[x][y]
            if material:
                material.update(x, y, grid)


def count_materials():
    material_count = {'sand': 0, 'water': 0, 'metal': 0}
    for row in grid:
        for cell in row:
            if isinstance(cell, Sand):
                material_count['sand'] += 1
            elif isinstance(cell, Water):
                material_count['water'] += 1
            elif isinstance(cell, Metal):
                material_count['metal'] += 1
    return material_count


def draw_text(text, pos):
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, pos)


running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обработка зажатых кнопок мыши
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    grid_x = mouse_x // CELL_SIZE
    grid_y = mouse_y // CELL_SIZE
    radius = 10
    if mouse_buttons[0]:  # Левая кнопка мыши зажата
        if grid_x < grid_width and grid_y < grid_height:
            for i in range(radius):
                for j in range(radius):
                    if 0 <= grid_x + i < grid_width and 0 <= grid_y + j < grid_height:
                        grid[grid_x + i][grid_y + j] = Sand()
    elif mouse_buttons[2]:  # Правая кнопка мыши зажата
        if grid_x < grid_width and grid_y < grid_height:
            for i in range(radius):
                for j in range(radius):
                    if 0 <= grid_x + i < grid_width and 0 <= grid_y + j < grid_height:
                        grid[grid_x + i][grid_y + j] = Water()
    elif mouse_buttons[1]:  # Средняя кнопка мыши зажата
        radius = 15
        if grid_x < grid_width and grid_y < grid_height:
            for i in range(radius):
                for j in range(radius):
                    if 0 <= grid_x + i < grid_width and 0 <= grid_y + j < grid_height:
                        grid[grid_x + i][grid_y + j] = Metal()
    update_grid()
    screen.fill(COLORS['empty'])
    draw_grid()

    # Подсчет и отображение количества блоков
    material_count = count_materials()
    draw_text(f"Sand: {material_count['sand']}", (10, 10))
    draw_text(f"Water: {material_count['water']}", (10, 50))
    draw_text(f"Metal: {material_count['metal']}", (10, 90))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
