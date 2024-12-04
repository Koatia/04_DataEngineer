"""
Задание №3
Погружение в Python | Функции

✔ Функция получает на вход строку из двух чисел через пробел.
✔ Сформируйте словарь, где ключом будет символ из Unicode, а значением — целое число.
✔ Диапазон пар ключ-значение от наименьшего из введённых пользователем чисел до наибольшего включительно.
"""

def string_to_dict(string: str):
    num = sorted(list(map(int, string.split())))
    print(string)

    result = {}
    for i in range(num[0], num[1] + 1):
        result[chr(i)] = i
    return result

txt = "957 32"
print(string_to_dict(txt))
