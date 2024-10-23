"""
Задача 1

Дан список повторяющихся элементов. Вернуть список с дублирующимися элементами.
В результирующем списке не должно быть дубликатов.
"""

myList = [2, 3, 6, 1, 8, 8, 1, 2, 5, 53, 4, 5, 6, 7, 8, 8, 8, 5, 5, 6, 6, 8, 8, 7, 2, 6, 1]
print(f"Задача 1\nИсходный список {myList= }")
myNewList = []
for item in set(myList):
    if myList.count(item) > 1:
        myNewList.append(item)
print(f"Cписок с дублирующимися элементами {myNewList= }")
"""
Задача 2

В большой текстовой строке подсчитать количество встречаемых слов и вернуть 10 самых частых.
Не учитывать знаки препинания и регистр символов.
За основу возьмите любую статью из википедии или из документации к языку.
"""

import urllib3
import re

url = "https://github.com/python/cpython/raw/refs/heads/main/Doc/reference/expressions.rst"
http = urllib3.PoolManager()
response = http.request('GET', url)
data = response.data

# Преобразование и очистка данных
data = str(data).replace("\\n", " ").replace("  ", " ")
newText = re.findall('[a-zа-яё]+', data.lower())

# for word in sorted(set(newText), key=newText.count, reverse=True)[:10]:
#     print(word, newText.count(word))

print(f"\nЗадача 2\n10 самых часто встречаемых слов в файле {url}")
print(*sorted(set(newText), key=newText.count, reverse=True)[:10], sep=' ')

"""
Задача 3

Создайте словарь со списком вещей для похода в качестве ключа и их массой в качестве значения.
Определите, какие вещи влезут в рюкзак, передав его максимальную грузоподъёмность.
Достаточно вернуть один допустимый вариант.
"""

from random import randint

# ves = int(input('Введите максимальную грузоподъёмность рюкзака: '))
LOWER_LIMIT = 9000
UPPER_LIMIT = 11000

ves = randint(LOWER_LIMIT, UPPER_LIMIT)
print(f"\nЗадача 3\nМаксимальная грузоподъёмность рюкзака: {ves}")

things = [('зажигалка', 20), ('компас', 100), ('фрукты', 500), ('рубашка', 300),
          ('термос', 1000), ('аптечка', 200), ('куртка', 600), ('бинокль', 400),
          ('удочка', 1200), ('салфетки', 40), ('бутерброды', 820), ('палатка', 5500),
          ('спальный мешок', 2250), ('жвачка', 10), ('котелок', 400), ('кружка', 100)]

# Сортируем по весу по убыванию
sortedThings = sorted(things, key=lambda x: x[1], reverse=True)

# Вещи, которые войдут в рюкзак
thingsInBag = []

# Перебираем список вещей
for thing in sortedThings[:]:  # [:] делаем копию списка
    if thing[1] <= ves:
        ves -= thing[1]  # Уменьшаем оставшийся вес рюкзака
        thingsInBag.append(thing)  # Добавляем вещь в рюкзак
        sortedThings.remove(thing)  # Удаляем вещь из исходного списка

print("Вещи в рюкзаке:", thingsInBag)
print("Оставшиеся вещи:", sortedThings)
print("Оставшийся вес:", ves)
