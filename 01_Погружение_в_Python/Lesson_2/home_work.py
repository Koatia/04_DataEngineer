"""
Задание 1. Напишите программу, которая получает целое число и возвращает его шестнадцатеричное строковое представление.
Функцию hex используйте для проверки своего результата.
"""
HEX = 16
HEX_CHAR = "0123456789abcdef"
num = int(input("Введите число: "))
check_num = f"Проверка:  {hex(num) = }"

result: str = ""
add_res: str = ""

while num > 0:
    result = HEX_CHAR[num % HEX] + result
    num //= HEX
print(f"For {HEX = } {result = }")

print(check_num)

# %%
"""
Задание 2. Напишите программу, которая принимает две строки вида “a/b” - дробь с числителем и знаменателем.
Программа должна возвращать сумму и произведение дробей.
Для проверки своего кода используйте модуль fractions
"""
import fractions
import math

frac_1 = str(input('Введите первое число вида a/b - ')).split('/')
frac_2 = str(input('Введите второе число вида a/b - ')).split('/')

# Сложение дробей с разными знаменателями
sum_frac = [int(frac_1[0]) * int(frac_2[1]) + int(frac_2[0]) * int(frac_1[1]),
            int(frac_1[1]) * int(frac_2[1])]
nod = math.gcd(sum_frac[0], sum_frac[1])  # Наименьший общий делитель
sum_frac = [int(sum_frac[0] / nod), int(sum_frac[1] / nod)]

# Умножение дробей и приведение к НОД
mult_frac = [int(frac_1[0]) * int(frac_2[0]),
             int(frac_1[1]) * int(frac_2[1])]
nod = math.gcd(mult_frac[0], mult_frac[1])
mult_frac = [int(mult_frac[0] / nod), int(mult_frac[1] / nod)]

firstfraction = fractions.Fraction(int(frac_1[0]), int(frac_1[1]))
secondfraction = fractions.Fraction(int(frac_2[0]), int(frac_2[1]))
result3 = firstfraction + secondfraction
result4 = firstfraction * secondfraction

print(f"Cумма дробей = {sum_frac[0]}/{sum_frac[1]}")
print(f"ПРОВЕРКА: Cумма дробей = {result3}")
print(f"Произведение дробей = {mult_frac[0]}/{mult_frac[1]}")
print(f"ПРОВЕРКА: Произведение дробей = {result4}")
