"""
Создайте функцию-генератор.
Функция генерирует N простых чисел, начиная с числа 2.
Для проверки числа на простоту используйте правило:
«число является простым, если делится нацело только на единицу и на себя».
"""

def prime_gen(n: int) -> (iter, int):
    current_number = 2
    while n > 0:
        if is_prime(current_number):
            n -= 1
            yield current_number
        current_number += 1

def is_prime(n: int) -> bool:
    if n % 2 == 0 and n != 2:
        return False
    for i in range(3, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

print(*prime_gen(5))
