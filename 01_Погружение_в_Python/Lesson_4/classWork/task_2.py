"""
Задание №2
Погружение в Python | Функции

✔ Напишите функцию, которая принимает строку текста.
✔ Сформируйте список с уникальными кодами Unicode каждого
символа введённой строки отсортированный по убыванию.
"""

txt = "Сформируйте список с уникальными кодами Unicode каждого символа введённой строки отсортированный по убыванию"

def string_to_unicode(string: str) -> list[int]:
    return sorted(set([ord(i) for i in string]), reverse=True)

def sentence_to_unicode(string: str) -> list[int]:
    result = []
    for symbol in string:
        result.append(ord(symbol))
    return sorted(result, reverse=True)

print(string_to_unicode(txt))
print(string_to_unicode(txt))