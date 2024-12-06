import pygame
from src.settings import WIDTH, HEIGHT, CELL_SIZE, grid_width, grid_height
from src.color_methods import COLORS
from src.materials.materials import Sand, Metal, Water

# Инициализация Pygame
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sand")
font = pygame.font.Font(None, 36)

grid = [[None for _ in range(grid_height)] for _ in range(grid_width)]


def create_metal_platform():
    # Определяем размеры платформы и ее местоположение
    platform_width = 150  # Ширина платформы в клетках
    platform_height = 5  # Высота платформы в клетках
    center_x = grid_width // 2
    center_y = grid_height // 2

    # Вычисляем начальные координаты платформы
    start_x = center_x - platform_width // 2
    start_y = center_y - platform_height // 2

    # Заполняем платформу металлом
    for x in range(start_x, start_x + platform_width):
        for y in range(start_y, start_y + platform_height):
            if 0 <= x < grid_width and 0 <= y < grid_height:
                grid[x][y] = Metal(x=x, y=y)


create_metal_platform()

current_material = Water
radius = 1
max_radius = 10


def draw_grid():
    for x in range(grid_width):
        for y in range(grid_height):
            material = grid[x][y]
            color = material.color if material else COLORS['empty']
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def update_grid():
    materials_to_update = []

    for y in range(grid_height - 1, -1, -1):

        for x in range(grid_width):
            material = grid[x][y]
            # if material and (not material.updated and material.frames_since_update < 3):
            if material and not material.updated:
                materials_to_update.append(material)
    for material in materials_to_update:
        result = material.update(grid)
        if result:
            material.updated = False


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


def add_material_to_grid(grid_x, grid_y, material_class, radius):
    if radius == 1:
        grid[grid_x][grid_y] = material_class(x=grid_x, y=grid_y)
    else:
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                distance_squared = i ** 2 + j ** 2
                if distance_squared <= radius ** 2:
                    # Проверяем, является ли материал металлом
                    if material_class.__name__ == "Metal":
                        # Для металла просто заполняем сферу
                        x = grid_x + i
                        y = grid_y + j
                        if 0 <= x < grid_width and 0 <= y < grid_height:
                            grid[x][y] = material_class(x=x, y=y)
                    else:
                        # Для других материалов создаем пробелы
                        if distance_squared % 2 == 0:  # Оставляем пробелы
                            x = grid_x + i
                            y = grid_y + j
                            if 0 <= x < grid_width and 0 <= y < grid_height:
                                grid[x][y] = material_class(x=x, y=y)


running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обработка колеса мыши
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Колесико вверх
                radius = min(radius + 1, max_radius)
            elif event.button == 5:  # Колесико вниз
                radius = max(radius - 1, 1)

        # Обработка нажатий клавиш
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_material = Sand
            elif event.key == pygame.K_2:
                current_material = Water
            elif event.key == pygame.K_3:
                current_material = Metal
            elif event.key == pygame.K_0:
                current_material = None

    # Обработка зажатых кнопок мыши
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    grid_x = mouse_x // CELL_SIZE
    grid_y = mouse_y // CELL_SIZE

    if mouse_buttons[0]:  # Левая кнопка мыши зажата
        if grid_x < grid_width and grid_y < grid_height:
            add_material_to_grid(grid_x, grid_y, current_material, radius)

    elif mouse_buttons[1]:  # Средняя кнопка мыши зажата
        if grid_x < grid_width and grid_y < grid_height:
            add_material_to_grid(grid_x, grid_y, Metal, 3)

    update_grid()
    screen.fill(COLORS['empty'])
    draw_grid()

    # Подсчет и отображение количества блоков
    material_count = count_materials()
    draw_text(f"Sand: {material_count['sand']}", (10, 10))
    draw_text(f"Water: {material_count['water']}", (10, 50))
    draw_text(f"Metal: {material_count['metal']}", (10, 90))
    draw_text(f"Radius: {radius}", (10, 130))  # Показываем текущий радиус

    # Отображение FPS
    fps = clock.get_fps()
    draw_text(f"FPS: {int(fps)}", (WIDTH - 100, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
