"""
Задание №7
Погружение в Python | Функции

✔ Функция получает на вход словарь с названием компании в качестве ключа
и списком с доходами и расходами (3-10 чисел) в качестве значения.
✔ Вычислите итоговую прибыль или убыток каждой компании. Если все компании
прибыльные, верните истину, а если хотя бы одна убыточная — ложь.
"""

from pprint import pprint

my_dict = {"company_1": [70, 12, 25, -28, 10, 36],
           "company_2": [-55, 10, -20, -10, -15, -15],
           "company_3": [40, 12, 21, -70, 11, 65]}

pprint(my_dict)

def task_7(dat: dict[str, list[int | float]]) -> bool:
    new_list = []
    for cur_list in dat.values():
        new_list.append(sum(cur_list) > 0)  # Положительное число - True
    return all(new_list)

print(task_7(my_dict))

# Второй вариант
print(all(sum(value) > 0 for value in my_dict.values()))

# Третий вариант
print(all(map(lambda x: sum(x) > 0, my_dict.values())))
