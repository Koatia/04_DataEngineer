"""
Задание №1
Погружение в Python | Функции

Напишите функцию, которая принимает строку текста. Вывести функцией каждое слово с новой строки.
✔ Строки нумеруются начиная с единицы.
✔ Слова выводятся отсортированными согласно кодировки Unicode.
✔ Текст выравнивается по правому краю так, чтобы у самого длинного слова был один пробел между ним и номером строки.
"""

sentence = "Шла Саша по шоссе и сосала сушку"


def print_sentence(string: str) -> None:
    string_split = sorted(string.split())
    max_len = len(max(string_split, key=len))
    for index, value in enumerate(string_split, 1):
        print(f"{index}. {value:>{max_len}} ")


print_sentence(sentence)
