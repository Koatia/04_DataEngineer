"""
Задание №5
✔ Напишите программу, которая решает квадратные уравнения даже если дискриминант отрицательный.
✔ Используйте комплексные числа для извлечения квадратного корня.
"""

print('Решение квадратного уравнения вида a*x**2+b*x+c=0')
a = 10
b = 10
c = 1

d = b ** 2 - 4 * a * c

if d > 0:
    x1 = (-b + d ** 0.5) / (2 * a)
    x2 = (-b - d ** 0.5) / (2 * a)
    result = f"Корни уравнения: {x1 = }; {x2 = }"
elif d == 0:
    x1 = -b / (2 * a)
    result = f"Корень уравнения: x = {x1:.3f = }"
else:
    d = complex(d, 0)
    x1 = (-b + d ** 0.5) / (2 * a)
    x2 = (-b - d ** 0.5) / (2 * a)
    result = f"У уравнения комплексные корни: {x1 = }; {x2 = }"

print(result)
