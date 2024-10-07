"""
Задание №8
Погружение в Python | Функции

✔ Создайте несколько переменных заканчивающихся и не оканчивающихся на «s».
✔ Напишите функцию, которая при запуске заменяет содержимое переменных
оканчивающихся на s (кроме переменной из одной буквы s) на None.
✔ Значения не удаляются, а помещаются в одноимённые переменные без s на конце.
"""
from pprint import pprint

names = ['Alex', 'Nick', 'Michael']
count = 1
tapes = 1500
txt = 'Test'
rows = 'first'
s = -15
sym_calls = True

pprint(globals())

def value_changer():
    globals_var = globals()
    new_dict = {}

    for key, value in globals_var.items():
        if key.endswith('s') and len(key) != "s":
            new_dict[key[:-1]] = value
            globals_var[key] = None

    for key, value in new_dict.items():
        globals_var[key] = value

value_changer()
pprint(globals())
