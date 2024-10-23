"""
Задание №4

Прочитайте созданный в прошлом задании csv файл без
использования csv.DictReader.
Дополните id до 10 цифр незначащими нулями.
В именах первую букву сделайте прописной.
Добавьте поле хеш на основе имени и идентификатора.
Получившиеся записи сохраните в json файл, где каждая строка
csv файла представлена как отдельный json словарь.
Имя исходного и конечного файлов передавайте как аргументы
функции.
"""

import csv
import json
import os
from pathlib import Path


def csv_to_json(csv_file: str | Path, json_file: str | Path) -> None:
    """ Получившиеся записи сохраняются в json файл, где каждая строка
    csv файла представлена как отдельный json словарь.
    :param csv_file:
    :param json_file:
    :return:
    """
    csv_file = Path.cwd() / csv_file
    if not os.path.isfile(csv_file):
        print(f'Файл {csv_file} не найден')
        return

    json_list = []
    with open(Path.cwd() / csv_file, 'r', encoding='utf-8', newline='') as csv_f:
        csv_reader = csv.reader(csv_f, dialect='excel-tab')
        for i, row in enumerate(csv_reader):
            if i == 0:  # пропускаем заголовки
                continue
            json_dict = {}
            level, user_id, name = row
            json_dict['level'] = int(level)
            json_dict['id'] = user_id.zfill(10)
            json_dict['name'] = name.title()
            json_dict['hash'] = hash(f"{json_dict['name']}{json_dict['id']}")
            json_list.append(json_dict)

    with open(Path.cwd() / json_file, 'w', encoding='utf-8') as json_f:
        json.dump(json_list, json_f, indent=2)

    print(f'данные конвертированы с {csv_file} в {json_file}')


if __name__ == '__main__':
    csv_to_json('users.csv', 'new_users.json')
