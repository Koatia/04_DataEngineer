"""
Задание №3
✔ Напишите функцию, которая открывает на чтение созданные в прошлых задачах файлы с числами и именами.
✔ Перемножьте пары чисел. В новый файл сохраните имя и произведение:
✔ если результат умножения отрицательный, сохраните имя записанное строчными буквами и произведение по модулю
✔ если результат умножения положительный, сохраните имя прописными буквами и произведение округлённое до целого.
✔ В результирующем файле должно быть столько же строк, сколько в более длинном файле.
✔ При достижении конца более короткого файла, возвращайтесь в его начало.
"""

from pathlib import Path
from typing import TextIO


def read_line_or_begin(fd: TextIO) -> str:
    text = fd.readline()
    if text == '':
        fd.seek(0)
        text = fd.readline()
    return text.rstrip()


def convert_lines(numbers: str | Path, names: str | Path, results: str | Path) -> None:
    with (
        open(names, 'r', encoding='utf-8') as f_names,
        open(numbers, 'r', encoding='utf-8') as f_numbers,
        open(results, 'a', encoding='utf-8') as f_results,
    ):
        len_names = sum(1 for _ in f_names)
        len_numbers = sum(1 for _ in f_numbers)
        max_len = max(len_names, len_numbers)

        # Reset file pointers to the beginning
        f_names.seek(0)
        f_numbers.seek(0)

        for _ in range(max_len):
            name = read_line_or_begin(f_names)
            nums_str = read_line_or_begin(f_numbers)
            num_i, num_f = map(float, nums_str.split())
            multiply = num_i * num_f
            if multiply < 0:
                f_results.write(f'{name.lower()} {-multiply}\n')
            elif multiply > 0:
                f_results.write(f'{name.upper()} {int(multiply)}\n')


if __name__ == '__main__':
    convert_lines(Path('task_1.txt'), Path('task_2.txt'), Path('task_3.txt'))
