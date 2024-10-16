"""
Выведите в консоль таблицу умножения от 2х2 до 9х10 как на школьной тетрадке.
Таблицу создайте в виде однострочного генератора,
где каждый элемент генератора — отдельный пример таблицы умножения.
Для вывода результата используйте «принт» без перехода на новую строку.
"""
LOWER_LIMIT = 2
UPPER_lIMIT = 10
COLUMN = 4
ONE = 1

def product_table() -> iter:
    for i in range(LOWER_LIMIT, UPPER_lIMIT, COLUMN):
        for j in range(LOWER_LIMIT, UPPER_lIMIT + 1):
            for k in range(i, i + COLUMN):
                if j == UPPER_lIMIT and k == i + COLUMN - 1:
                    print(f'{k:>} x {j:>2} = {k * j:>2}\n\n', end='')
                elif k == i + COLUMN - 1:
                    print(f'{k:>} x {j:>2} = {k * j:>2}\n', end='')
                else:
                    print(f'{k:>} x {j:>2} = {k * j:>2}\t\t', end='')

def product_table2() -> iter:
    for i_main in (LOWER_LIMIT, LOWER_LIMIT + COLUMN):
        for s_num in range(LOWER_LIMIT, UPPER_lIMIT + ONE):
            for f_num in range(i_main, i_main + COLUMN):
                print(f'{f_num:>2} x {s_num:>2} = {f_num * s_num:>2}', end='\t')
            print()
        print()

table_generator = (f'{f_num:>2} x {s_num:>2} = {f_num * s_num:>2}\t' if f_num < i_main + COLUMN - ONE else
                   f"{f_num:>2} x {s_num:>2} = {f_num * s_num:>2}\n" if s_num < UPPER_lIMIT else
                   f"{f_num:>2} x {s_num:>2} = {f_num * s_num:>2}\n\n"
                   for i_main in (LOWER_LIMIT, LOWER_LIMIT + COLUMN)
                   for s_num in range(LOWER_LIMIT, UPPER_lIMIT + ONE)
                   for f_num in range(i_main, i_main + COLUMN))

# product_table()
# product_table2()

print(*table_generator)
