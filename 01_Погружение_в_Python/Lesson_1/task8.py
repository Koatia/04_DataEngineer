# Задание 8

"""
Нарисовать в консоли елку, спросив у пользователя количество рядов
Например:

Сколько рядов у елки? 5
    *
   ***
  *****
 *******
*********
"""

SPACE = " "
STAR = "*"
ONE = 1

rows = int(input("Сколько рядов у елки? "))
spases = rows - ONE
stars = ONE

for i in range(0, rows):
    print(spases * SPACE + stars * STAR)
    spases -= ONE
    stars += ONE + ONE
