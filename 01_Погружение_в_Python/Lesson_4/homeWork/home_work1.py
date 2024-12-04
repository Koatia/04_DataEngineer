"""
Task 1.

Напишите функцию для транспонирования матрицы
"""

input_data = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 0],
    [11, 12, 13, 14, 15]
]


def rotation_matrix(in_matrix):
    """Функцию для транспонирования матрицы"""

    row = len(in_matrix)
    col = len(in_matrix[0])

    # Инициализируем новую матрицу нужного размера
    new_matrix = [[0] * row for _ in range(col)]

    for i in range(row):
        for j in range(col):
            new_matrix[j][i] = in_matrix[i][j]
    return new_matrix


def print_matrix(matrix):
    """Функцию для вывода в консоль матрицы"""
    for row in matrix:
        print(row)


print_matrix(input_data)
print_matrix(rotation_matrix(input_data))
