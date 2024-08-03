# def move_along_path(path):
#     for i in range(len(path)):
#         cell = path[i]
#
#         if cell == "препятствие":
#             print(f"Препятствие обнаружено на позиции {i}. Остановка.")
#             break  # Прекратить движение при обнаружении препятствия
#
#         # Обработка текущей клетки
#         print(f"Двигаемся по клетке {i}")
#
#     else:
#         print("Достигнут конец пути без препятствий.")
#
#
# path = ["пусто", "пусто", "пусто", "пусто"]
# move_along_path(path)
import math

vel_y = 221
vel_x = 11

# Расчет absY
absY = max(abs(vel_y) / 31, 105)

# Обновление vel.x
vel_x = -absY if vel_x < 0 else absY

print(f'Updated vel.x: {vel_x}')
