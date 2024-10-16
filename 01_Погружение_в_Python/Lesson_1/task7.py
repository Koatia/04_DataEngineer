# Задание 7

"""
Пользователь вводит число от 1 до 999. Используя операцию с числами, сообщите, что введено цифра, двухзначное число или трехзначное число.
Для цифры введите и верните ее квадрат, например, 5 - 25.
Для двухзначного числа произведение цифр. Например, 30 - 0.
Для трехзначного числа его зеркальное отображение. Например, 520 - 25.
Если число не из диапазона, запросите новое число.
Откажитесь от магических чисел.
В коде должны быть один input и один print.
"""

LOWER_LIMIT = 1
UPPER_LIMIT = 999
ONE = 1
TEN = 10
HUNDRED = 100

num = 0

while num < LOWER_LIMIT or num > UPPER_LIMIT:
    num = int(input(f"Введите число от {LOWER_LIMIT} до {UPPER_LIMIT}: "))

if num < TEN:
    res = f"Число {num} - цифра. Её квадрат = {num * num}"
elif num < HUNDRED:
    firstNum = num // TEN
    secondNum = num % TEN
    res = f"Число {num} - двухзначное. Произведение цифр = {firstNum * secondNum}"
else:
    firstNum = num // HUNDRED
    secondNum = num // TEN % TEN
    thirdNum = num % TEN
    mirror = (thirdNum * HUNDRED + secondNum * TEN + firstNum)
    res = f"Число {num} - трехзначное. Его зеркальное отображение = {mirror}"

print(res)
