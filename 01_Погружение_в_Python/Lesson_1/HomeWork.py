"""
1. Треугольник существует только тогда, когда сумма любых двух его сторон больше третьей.
Дано a, b, c - стороны предполагаемого треугольника.
Требуется сравнить длину каждого отрезка-стороны с суммой двух других.
Если хотя бы в одном случае отрезок окажется больше суммы двух других, то треугольника с такими сторонами не существует.
Отдельно сообщить является ли треугольник разносторонним, равнобедренным или равносторонним.
"""
a, b, c = map(int, input("Введите длину каждой из сторон треугольника через пробел: ").split())

if (a > (b + c)) or (b > (a + c)) or (c > (b + a)):
    res = f"Треугольника со сторонами a={a} b={b} c={c + a + b} не существует"
elif a == b and b == c:
    res = f"Треугольник со сторонами a={a} b={b} c={c} равносторонний"
elif a == b or b == c or c == a:
    res = f"Треугольник со сторонами a={a} b={b} c={c} равнобедренный"
else:
    res = f"Треугольник со сторонами a={a} b={b} c={c} разносторонний"

print(res)

# %%
"""
2. Напишите код, который запрашивает число и сообщает, является ли оно простым или составным.
Используйте правило для проверки: “Число является простым, если делится нацело только на единицу и на себя”.
Сделайте ограничение на ввод отрицательных чисел и чисел больше 100 тысяч.
"""
MINIMAL = 1
MAXIMAL = 100000

number = -1
while number < MINIMAL or number > MAXIMAL:
    number = int(input(f'Введите число от {MINIMAL} до {MAXIMAL}: '))

res = f"Число {number} простое"
for i in range(2, int(number ** 0.5) + 1):
    if number % i == 0:
        res = f"Число {number} составное"
        break

print(res)

# %%
"""
3. Программа загадывает число от 0 до 1000. Необходимо угадать число за 10 попыток.
Программа должна подсказывать “больше” или “меньше” после каждой попытки.
Для генерации случайного числа используйте код:
from random import randint
num = randint(LOWER_LIMIT, UPPER_LIMIT)
"""
LOWER_LIMIT = 0
UPPER_LIMIT = 1000
from random import randint

num = randint(LOWER_LIMIT, UPPER_LIMIT)
number = int(input(f'Введите число от {LOWER_LIMIT} до {UPPER_LIMIT}: '))

while number != num:
    if number < num:
        print(f"Ваше число {number} меньше загаданного")
    else:
        print(f"Ваше число {number} больше загаданного")
    number = int(input(f'Введите число от {LOWER_LIMIT} до {UPPER_LIMIT}: '))

print(f"Вы угадали загаданное число {number}")

# %%
"""
3. Программа загадывает число от 0 до 1000 и сама угадывает его
"""
LOWER_LIMIT = 0
UPPER_LIMIT = 1000
from random import randint

num = randint(LOWER_LIMIT, UPPER_LIMIT)

number = int((LOWER_LIMIT + UPPER_LIMIT) / 2)

while number != num:
    if number < num:
        print(f"Ваше число {number} меньше загаданного")
        LOWER_LIMIT = number + 1
    else:
        print(f"Ваше число {number} больше загаданного")
        UPPER_LIMIT = number - 1
    number = int((LOWER_LIMIT + UPPER_LIMIT) / 2)

print(f"Вы угадали загаданное число {number}")
