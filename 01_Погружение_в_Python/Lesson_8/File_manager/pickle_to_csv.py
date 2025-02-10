"""
Задание 6

- Напишите функцию, которая преобразует pickle файл хранящий список словарей в табличный csv файл.
- Для тестирования возьмите pickle версию файла из задачи 4 этого семинара.
- Функция должна извлекать ключи словаря для заголовков столбца из переданного файла.
"""

import csv
import os
import pickle
from pathlib import Path

def pickle_to_csv(file: str | Path):
    """Преобразует pickle файл, хранящий список словарей, в табличный csv файл"""
    file = Path.cwd() / file
    if os.path.isfile(file):  # проверка на наличие файла
        with (
            open(file, 'rb') as f_read,
            open(f'{file.stem}.csv', 'w', encoding='utf-8', newline='') as f_write
            ):
            data = pickle.load(f_read)
            headers_list = list(data[0].keys())
            csv_writer = csv.DictWriter(f_write, fieldnames=headers_list, dialect='excel-tab',
                                        quoting=csv.QUOTE_NONNUMERIC)
            csv_writer.writeheader()
            csv_writer.writerows(data)

if __name__ == '__main__':
    pickle_to_csv('new_users.pickle')
