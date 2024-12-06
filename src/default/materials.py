import math

from src.default.move import find_last_free_position
import random
from src.settings import grid_width, grid_height


class Material:
    def __init__(self, name, color, condition, x, y, mass=0, friction=10, falling_speed=0.12, updated=False,
                 dispersion_rate=1, horizontal_speed=0, gravity=0.5, max_horizontal_speed=3, frames_since_update=0,
        density = 1, buoyancy = 1):

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
        self.max_horizontal_speed = max_horizontal_speed
        self.frames_since_update = frames_since_update
        self.density = density
        self.buoyancy = buoyancy
    def update(self, grid):
        pass

    def move_down(self, x, y, grid):

        grid[x][y], grid[x][y + 1] = None, self
        self.x, self.y = x, y + 1
        self.falling_speed += 0.1

        ##############################

        self.frames_since_update = 0

    def swap_materials(self, x, y, grid, target_cell):
        grid[x][y], grid[x][y + 1] = target_cell, self
        self.x, self.y = x, y + 1
        target_cell.x, target_cell.y = x, y
        self.frames_since_update = 0

    def diagonal_move(self, x, y, grid):
        if y + 1 < grid_height and x > 0 and grid[x - 1][y + 1] is None:
            grid[x][y], grid[x - 1][y + 1] = None, self
            self.x, self.y = x - 1, y + 1
            self.frames_since_update = 0
            return True

        elif y + 1 < grid_height and x < grid_width - 1 and grid[x + 1][y + 1] is None:
            grid[x][y], grid[x + 1][y + 1] = None, self
            self.x, self.y = x + 1, y + 1
            self.frames_since_update = 0
            return True
        return False


class Solid(Material):
    def __init__(self, name, color, x, y, mass=1):
        super().__init__(name, color, 'Solid', x, y, mass=1, friction=30)

class MoveSolid(Solid):
    def __init__(self, name, color, x, y):
        super().__init__(name, color, x, y, mass=1)
        self.falling_speed = 0.2
        self.horizontal_speed = 0  # Начальная горизонтальная скорость
        self.max_horizontal_speed = 3  # Максимальная горизонтальная скорость
        self.friction = 0.7  # Трение для затухания инерции
        self.min_falling_speed = 0.05  # Минимальная скорость падения
        self.direction = None  # Направление движения
        self.direction_set = False  # Флаг, что направление задано

    def update(self, grid):
        x, y = self.x, self.y

        if y + 1 < grid_height:
            target_cell = grid[x][y + 1]
            if target_cell is None:
                # Если клетка снизу свободна, падаем
                self.move_down(x, y, grid)

            elif isinstance(target_cell, Liquid):
                # Если снизу жидкость, меняемся местами
                self.swap_materials(x, y, grid, target_cell)

            elif isinstance(target_cell, Solid):
                # Если снизу твердый материал, пробуем сдвинуться по диагонали
                move = self.diagonal_move(x, y, grid)

                # Если не удалось переместиться диагонально
                if not move and self.falling_speed > 0 or (not move and self.horizontal_speed != 0):
                    # Уменьшаем скорость падения после столкновения с твердым материалом
                    self.falling_speed = max(self.min_falling_speed, self.falling_speed - 0.05)

                    # Если горизонтальная инерция еще не была задана, запускаем её
                    if self.horizontal_speed == 0 and not self.direction_set:
                        # Задаем инерцию на основе текущей скорости падения
                        self.horizontal_speed = random.choice([-1, 1]) * self.falling_speed
                        self.falling_speed = 0
                        # Устанавливаем направление один раз
                        self.direction = int(math.copysign(1, self.horizontal_speed))
                        self.direction_set = True  # Закрепляем выбранное направление

                    new_x = x + self.direction
                    print(self.direction)
                    # Проверяем, можно ли двигаться в сторону
                    if 0 <= new_x < len(grid) and grid[new_x][y] is None:
                        # Перемещаемся в сторону
                        grid[new_x][y], grid[x][y] = self, None
                        self.x, self.y = new_x, y

                    # Уменьшаем горизонтальную скорость с учетом трения
                    self.horizontal_speed -= self.friction * self.direction

                    # Если скорость становится слишком маленькой, обнуляем её и сбрасываем флаг направления
                    if abs(self.horizontal_speed) < self.friction:
                        self.horizontal_speed = 0
                        self.direction_set = False  # Сбрасываем флаг направления, когда скорость обнулилась

        # if not self.direction_set:
        #     direction = None
        #
        # if self.direction is not None:
        #     print(self.horizontal_speed, self.falling_speed, self.direction)

        # Увеличиваем счетчик обновлений
        self.frames_since_update += 1
        return True

class Liquid(Material):
    def __init__(self, name, color, x, y):
        self.dispersion_rate = 4
        self.falling_speed = 0.24
        self.horizontal_speed = 0
        self.max_horizontal_speed = 3
        super().__init__(name, color, 'Liquid', x, y, 
                        dispersion_rate=self.dispersion_rate,
                        falling_speed=self.falling_speed, 
                        mass=1)

    def update(self, grid):
        x, y = self.x, self.y
        grid_height = len(grid[0])
        
        # Проверка возможности движения вниз
        if y + 1 < grid_height and not grid[x][y + 1]:
            self.move_down(x, y, grid)
        else:
            # Горизонтальное движение
            direction = random.choice([-1, 1])
            target_x = find_last_free_position(x, y, direction, self.dispersion_rate, grid)
            
            if target_x != x:
                self.horizontal_speed = target_x - x
                grid[target_x][y], grid[x][y] = self, None
                self.x, self.y = target_x, y
        
        self.frames_since_update += 1
        return True
