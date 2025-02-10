"""
Задание №6
Погружение в Python | Функции

Функция получает на вход список чисел и два индекса.
✔ Вернуть сумму чисел между переданными индексами.
✔ Если индекс выходит за пределы списка, сумма считается до конца и/или начала списка.
"""

def sum_range(lst: list[int | float], i1: int, i2: int) -> int | float:
    start = min(i1, i2)
    start = max(start, 0)

    end = max(i1, i2)
    end = min(end, len(lst))

    return sum(lst[start:end])

lst = [4, 8, 15, 16, 23, 42]

print(sum_range(lst, -2, 1))
