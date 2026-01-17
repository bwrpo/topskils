import random

# Шаг 1: Создание двумерного массива 6x8 со случайными числами от -10 до 10
rows, cols = 8, 6
matrix = [[random.randint(-3, 20) for _ in range(cols)] for _ in range(rows)]

# Вывод исходного массива (опционально)
print("Исходный массив:")
for row in matrix:
    print(row)

# Шаг 2: Формирование одномерного массива
result = []
for i in range(rows):
    found = False
    for j in range(cols):
        if matrix[i][j] >= 0:
            found = True
          
    if found == True:
        result.append(-1)
    else:
        result.append(1)
# Вывод результата
print("\nОдномерный массив:")
print(result)
