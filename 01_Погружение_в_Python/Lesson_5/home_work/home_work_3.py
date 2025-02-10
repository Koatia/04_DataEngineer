"""
Создайте функцию генератор чисел Фибоначчи.
"""


def func(number: int) -> (iter, int):
    """Функция - генератор чисел Фибоначчи """
    fibo_list = [0, 1, 1]
    count = 0
    while count < number:
        while len(fibo_list) < number:
            fibo_list.append(sum(fibo_list[-2:]))
        yield fibo_list[count]
        count += 1


print(*func(5))
