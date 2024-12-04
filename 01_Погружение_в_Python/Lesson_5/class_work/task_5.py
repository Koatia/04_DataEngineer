"""
Задание 5

Напишите программу, которая выводит на экран числа от 1 до 100.
- При этом вместо чисел, кратных трем, программа должна выводить слово «Fizz»
- Вместо чисел, кратных пяти — слово «Buzz».
- Если число кратно и 3, и 5, то программа должна выводить слово «FizzBuzz».
*Превратите решение в генераторное выражение.
"""
fizzbuzz = []
for number in range(1, 100):
    if number % 15 == 0:
        fizzbuzz.append("FizzBuzz")
    elif number % 3 == 0:
        fizzbuzz.append("Fizz")
    elif number % 5 == 0:
        fizzbuzz.append("Buzz")
    else:
        fizzbuzz.append(str(number))

print(*fizzbuzz)

fizzbuzz_gen = ("FizzBuzz" if number % 15 == 0 else
                "Fizz" if number % 3 == 0 else
                "Buzz" if number % 5 == 0 else number
                for number in range(1, 100))
print(*fizzbuzz_gen)
