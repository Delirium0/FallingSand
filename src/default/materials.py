import math

from src.default.move import find_last_free_position
import random
from src.settings import grid_width, grid_height


class Material:
    def __init__(self, name, color, condition, x, y, mass=0, friction=10, falling_speed=0.12, updated=False,
                 dispersion_rate=1, horizontal_speed=0, gravity=0.5):
        self.name = name
        self.color = color
        self.condition = condition
        self.x = x
        self.y = y
        self.dispersion_rate = dispersion_rate
        self.updated = updated
        self.falling_speed = falling_speed
        self.friction = friction
        self.mass = mass
        self.horizontal_speed = horizontal_speed
        self.gravity = gravity

    def update(self, grid):
        pass

    def move_down(self, x, y, grid):

        grid[x][y], grid[x][y + 1] = None, self
        self.x, self.y = x, y + 1
        self.falling_speed += 0.1

        ##############################

    def swap_materials(self, x, y, grid, target_cell):
        grid[x][y], grid[x][y + 1] = target_cell, self
        self.x, self.y = x, y + 1
        target_cell.x, target_cell.y = x, y

    def diagonal_move(self, x, y, grid):
        if y + 1 < grid_height and x > 0 and grid[x - 1][y + 1] is None:
            grid[x][y], grid[x - 1][y + 1] = None, self
            self.x, self.y = x - 1, y + 1
            return True

        elif y + 1 < grid_height and x < grid_width - 1 and grid[x + 1][y + 1] is None:
            grid[x][y], grid[x + 1][y + 1] = None, self
            self.x, self.y = x + 1, y + 1
            return True
        return False


class Solid(Material):
    def __init__(self, name, color, x, y, mass=1):
        super().__init__(name, color, 'Solid', x, y, mass=1, friction=30)


class MoveSolid(Solid):
    def __init__(self, name, color, x, y):
        super().__init__(name, color, x, y, mass=1)
        self.falling_speed = 0.2

    def update(self, grid):
        x, y = self.x, self.y

        if y + 1 < grid_height:
            target_cell = grid[x][y + 1]
            if target_cell is None:
                self.move_down(x, y, grid)
            elif isinstance(target_cell, Liquid):
                self.swap_materials(x, y, grid, target_cell)
            elif isinstance(target_cell, Solid):
                move = self.diagonal_move(x, y, grid)

                # Если не удалось переместиться диагонально, рассчитываем горизонтальную скорость
                if self.falling_speed > 0:
                    if self.horizontal_speed == 0:
                        self.falling_speed = 0
                        abs_y = max(abs(self.falling_speed) / 31, 105)
                        direction = random.choice([-1, 1])
                        self.horizontal_speed = abs_y * direction
                    else:
                        # Уменьшаем горизонтальную скорость с учетом трения
                        friction_effect = self.friction * math.copysign(1, self.horizontal_speed)
                        self.horizontal_speed -= friction_effect

                        # Если скорость близка к нулю, установите ее в 0
                        if abs(self.horizontal_speed) < self.friction:
                            self.horizontal_speed = 0

                # Перемещение частицы
                if not move:
                    print(self.horizontal_speed)
                    if self.horizontal_speed != 0:
                        direction = int(math.copysign(1, self.horizontal_speed))
                        new_x = x + direction
                        if 0 <= new_x < len(grid) and grid[new_x][y] is None:
                            grid[new_x][y], grid[x][y] = self, None
                            self.x, self.y = new_x, y
                            # Обновляем горизонтальную скорость с учетом трения
                            self.horizontal_speed -= self.friction * direction

                            # Проверяем, если после перемещения скорость всё еще велика
                            if abs(self.horizontal_speed) < self.friction:
                                self.horizontal_speed = 0

        return True


class Liquid(Material):
    def __init__(self, name, color, x, y):
        self.dispersion_rate = 2
        self.falling_speed = 0.24
        super().__init__(name, color, 'Liquid', x, y, dispersion_rate=self.dispersion_rate,
                         falling_speed=self.falling_speed, mass=1)

    def update(self, grid):
        x, y = self.x, self.y
        if y + 1 < len(grid[0]) and grid[x][y + 1] is None:
            self.move_down(x, y, grid)

        else:
            direction = random.choice([-1, 1])

            target_x = find_last_free_position(x, y, direction, self.dispersion_rate, grid)

            if target_x != x:
                grid[target_x][y], grid[x][y] = self, None
                self.x, self.y = target_x, y
        return True
