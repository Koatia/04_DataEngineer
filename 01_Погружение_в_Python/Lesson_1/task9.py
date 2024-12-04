"""
Задание 9

Вывести в консоль таблицу умножения от 2х2 до 9х10 как в школьной тетрадке.
"""

LOWER_LIMIT = 2
UPPER_LIMIT = 10
COLUMN = 4
ONE = 1

for i_main in (LOWER_LIMIT, LOWER_LIMIT + COLUMN):
    for sNum in range(LOWER_LIMIT, UPPER_LIMIT + ONE):
        for fNum in range(i_main, COLUMN + i_main):
            print(f"{fNum:>2} x {sNum:<2} = {fNum * sNum:<2}", end="\t")
        print()
    print()
