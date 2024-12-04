"""
Задача №3

Создайте вручную кортеж содержащий элементы разных типов. Получите из него словарь списков, где: ключ — тип элемента,
значение — список элементов данного типа.
"""

data = (1, 2.3, 'hi', True, 'Hello', 5, None, False)
myDict = {}

for item in data:
    myDict.setdefault(type(item), []).append(item)


print(myDict)  # можно так вывести,

for key in myDict:
    print(f"type: {key}  value: {myDict[key]} ")  # а можно перебрать попарно
