"""
Задание 7

- Прочитайте созданный в прошлом задании csv файл без использования csv.DictReader.
- Распечатайте его как pickle строку.
"""

import csv
import os
from pathlib import Path


def csv_to_pickle(file: str | Path) -> None:
    """
    Читает созданный csv файл без использования csv.DictReader. Распечатывает его как pickle строку.
    :param file:
    :return:
    """
    file = Path.cwd() / file
    pickle_list = []
    if os.path.isfile(file):  # проверка на наличие файла
        with open(file, 'r', encoding='utf-8') as f_read:
            csv_reader = csv.reader(f_read, dialect='excel-tab')
            for i, row in enumerate(csv_reader):
                if i == 0:
                    pickle_keys = row
                else:
                    pickle_dict = {k: v for k, v in zip(pickle_keys, row)}
                    pickle_list.append(pickle_dict)
        print(pickle_list)


if __name__ == '__main__':
    csv_to_pickle('new_users.csv')
