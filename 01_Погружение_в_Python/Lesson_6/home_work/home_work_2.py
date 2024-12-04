"""
Задача 2

Добавьте в пакет, созданный на семинаре шахматный модуль. Внутри него напишите код, решающий задачу о 8 ферзях.
Известно, что на доске 8×8 можно расставить 8 ферзей так, чтобы они не били друг друга. Вам дана расстановка
8 ферзей на доске, определите, есть ли среди них пара бьющих друг друга. Программа получает на вход восемь пар чисел,
 каждое число от 1 до 8 - координаты 8 ферзей. Если ферзи не бьют друг друга верните истину, а если бьют - ложь. .
'''

'''
Задача 3

Напишите функцию в шахматный модуль. Используйте генератор случайных чисел для случайной расстановки ферзей в задаче выше.
Проверяйте различный случайные варианты и выведите 4 успешных расстановки.
"""
import random

def is_queen_beat(position: list[(int, int)]) -> bool:
    """Если ферзи не бьют друг друга возвращает истину, а если бьют - ложь"""
    n = 8
    x = []
    y = []

    for i in range(n):
        x.append(position[i][0])
        y.append(position[i][1])

    for i in range(n - 1):
        for j in range(i + 1, n):
            if (x[i] == x[j]
                    or y[i] == y[j]
                    or abs(x[i] - x[j]) == abs(y[i] - y[j])):
                return False  # ферзи бьют друг друга
    return True  # ферзи не бьют друг друга

def generate_position(count_successful):
    position = []
    n = 8
    count = 1
    count_iter = 0
    while count <= count_successful:
        count_iter += 1
        i = 0
        for x in range(1, n + 1):
                y = random.randint(1, 8)
                if [x, y] not in position:
                    position.append((x, y))
                    i += 1

        if is_queen_beat(position):
            print(position, 'iter = ', count_iter)
            count += 1
        position.clear()

if __name__ == '__main__':
    solution = [(1, 1), (2, 5), (3, 8), (4, 6), (5, 3), (6, 7), (7, 2), (8, 4)]
    print(is_queen_beat(solution))

    generate_position(4)
