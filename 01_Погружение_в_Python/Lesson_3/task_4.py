"""
Задача №4

Создайте вручную список с повторяющимися элементами. Удалите из него все элементы, которые встречаются дважды.
"""

myList = [1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 5, 5, 6, 6, 8, 8, 7, 2, 6, 1]
COUNT = 2
print(f"{myList=}")

for item in set(myList):
    if myList.count(item) == COUNT:
        print(item)
        for _ in range(COUNT):
            myList.remove(item)

print(f"{myList=}")
