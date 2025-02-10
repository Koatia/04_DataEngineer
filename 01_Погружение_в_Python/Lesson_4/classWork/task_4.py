"""
Задание №4
Погружение в Python | Функции

✔ Функция получает на вход список чисел.
✔ Отсортируйте его элементы in place без использования встроенных в язык сортировок.
✔ Как вариант напишите сортировку пузырьком. Её описание есть в википедии.
"""

import random


def bubble_sort(lst):
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst

lst = [random.randint(-100, 100) for i in range(100)]
print(lst)

print(bubble_sort(lst))

