"""
Задание №2

Напишите функцию, которая в бесконечном цикле
запрашивает имя, личный идентификатор и уровень доступа (от 1 до 7).
После каждого ввода добавляйте новую информацию в JSON файл.
Пользователи группируются по уровню доступа.
Идентификатор пользователя выступает ключём для имени.
Убедитесь, что все идентификаторы уникальны независимо от уровня доступа.
При перезапуске функции уже записанные в файл данные должны сохраняться.

Есть внешний словарь working_dict[access_level] с ключом access_level.
Внутри каждого ключа есть словарь с ключом Id, значением имя
"""

import json
from pathlib import Path


def set_users(file: str | Path) -> None:
    """Ввод данных с клавиатуры и сохранение их в JSON файл"""
    file = Path.cwd() / file
    u_ids = set()
    if not file.exists():
        data = {i: {} for i in range(1, 7 + 1)}
    else:
        with open(file, 'r', encoding='utf-8') as f_read:
            data = json.load(f_read)
        for value in data.values():
            u_ids.update(value.keys())
    while True:
        name = input('Введите имя: ')
        if not name:
            break
        id = input('Введите id: ')
        lvl = int(input('Введите уровень от 1 до 7: '))

        if not id in u_ids:
            # if not id in u_ids and data[lvl].get(id) is not None:
            data[lvl].update({id: name})
            with open(file, 'w', encoding='utf-8') as f_write:
                json.dump(data, f_write, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    set_users('users.json')
