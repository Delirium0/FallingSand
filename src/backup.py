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
                    print('лево')
                elif y + 1 < grid_height and x < grid_width - 1 and grid[x + 1][y + 1] is None:
                    grid[x][y], grid[x + 1][y + 1] = None, self
                    print('право')


class Liquid(Material):
    def __init__(self, name, color):
        self.dispersion_rape = 5
        super().__init__(name, color, 'Liquid', self.dispersion_rape)

    def update(self, x, y, grid):
        # тут просто вниз
        if y + 1 < grid_height and grid[x][y + 1] is None:
            grid[x][y], grid[x][y + 1] = None, self
        # тут по диагонали
        elif y + 1 < grid_height and x > 0 and grid[x - 1][y + 1] is None:
            grid[x][y], grid[x - 1][y + 1] = None, self
        elif y + 1 < grid_height and x < grid_width - 1 and grid[x + 1][y + 1] is None:
            grid[x][y], grid[x + 1][y + 1] = None, self

        else:
            direction = random.choice([-1, 1])

            if direction == -1:
                if 0 < x and grid[x - 1][y] is None:
                    grid[x][y], grid[x - 1][y] = None, self

            else:
                if x < grid_width - 1 and grid[x + 1][y] is None:
                    grid[x][y], grid[x + 1][y] = None, self
                # print(dispersion_range, direction, x + direction * dispersion_range)
                # if 0 <= x + direction < grid_width and grid[x + direction][y] is None:
                #     if self.dispersion_rape == dispersion_range + 1:
                #         grid[x][y], grid[x + direction * dispersion_range][y] = None, self
                # else:
                #     grid[x][y], grid[x + direction * dispersion_range][y] = None, self
                #     break
            ###########################################################
            # if 0 <= x + direction < grid_width and grid[x + direction][y] is None:
            #     grid[x][y], grid[x + direction][y] = None, self


class Sand(MoveSolid):
    def __init__(self):
        super().__init__('sand', COLORS['sand'])

    # def update(self, x, y, grid):
    #
    #     if y + 1 < grid_height and grid[x][y + 1] is None:
    #         grid[x][y], grid[x][y + 1] = None, self
    #     elif y + 1 < grid_height and isinstance(grid[x][y + 1], Water):
    #         grid[x][y], grid[x][y + 1] = grid[x][y + 1], self
    #     elif y + 1 < grid_height and x > 0 and grid[x - 1][y + 1] is None:
    #         grid[x][y], grid[x - 1][y + 1] = None, self
    #     elif y + 1 < grid_height and x < grid_width - 1 and grid[x + 1][y + 1] is None:
    #         grid[x][y], grid[x + 1][y + 1] = None, self


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


running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            grid_x = mx // CELL_SIZE
            grid_y = my // CELL_SIZE
            radius = 10

            if grid_x < grid_width and grid_y < grid_height:
                if event.button == 1:  # Левая кнопка мыши
                    for i in range(radius):
                        for j in range(radius):
                            grid[grid_x + i][grid_y + j] = Sand()
                elif event.button == 3:  # Правая кнопка мыши

                    for i in range(radius):
                        for j in range(radius):
                            grid[grid_x + i][grid_y + j] = Water()
                elif event.button == 2:  # Правая кнопка мыши
                    radius = 15
                    for i in range(radius):
                        for j in range(radius):
                            grid[grid_x + i][grid_y + j] = Metal()

    update_grid()
    screen.fill(COLORS['empty'])
    draw_grid()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
