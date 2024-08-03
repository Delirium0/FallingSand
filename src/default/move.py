import random


def find_last_free_position(x, y, direction, dispersion_rate, grid):
    last_free_x = x

    steps = random.randint(1, dispersion_rate)
    for i in range(1, steps + 1):
        new_x = x + i * direction
        if 0 <= new_x < len(grid) and grid[new_x][y] is None:
            last_free_x = new_x
        else:
            break

    return last_free_x
