"""
Задание №3

Напишите функцию, которая сохраняет созданный в прошлом задании файл в формате CSV.
"""

import csv
import json
import os
from pathlib import Path


def json_to_csv(file: str | Path) -> None:
    """Перенос данных из json в csv"""
    file = Path.cwd() / file

    if not os.path.isfile(file):
        print(f'Файл {file} не найден')
        return
    with open(file, 'r', encoding='utf-8') as js:
        if os.path.getsize(file) > 0:
            json_dict = json.load(js)

    list_row = []
    for level, id_name_dict in json_dict.items():
        for id, name in id_name_dict.items():
            list_row.append({'level': int(level), 'user_id': int(id), 'name': name})  # список словарей

    with open(f"{file.stem}.csv", 'w', newline='', encoding='utf-8') as f_write:
        csv_write = csv.DictWriter(f_write, fieldnames=['level', 'user_id', 'name'], dialect='excel-tab')
        csv_write.writeheader()  # сохранение первой строки с заголовком
        csv_write.writerows(list_row)  # сохранение списка словарей в формате csv в файл

    print(f'данные конвертированы с {file} в {file.stem}.csv')


if __name__ == '__main__':
    json_to_csv('users.json')
