"""
Задание 5

Напишите функцию, которая ищет json файлы в указанной директории
и сохраняет их содержимое в виде одноимённых pickle файлов.
"""

import json
import pickle
from pathlib import Path


def json_to_pickle(file: Path | str) -> None:
    """
    Ищет json файлы в указанной директории и сохраняет их содержимое в виде одноимённых pickle файлов
    :param file:
    :return:
    """
    for file in Path(file).glob('*.json'):
        with open(file, 'r', encoding='utf-8') as f_read:
            data = json.load(f_read)
        with open(f'{file.stem}.pickle', 'wb') as f_write:
            pickle.dump(data, f_write)


if __name__ == '__main__':
    json_to_pickle(Path.cwd())
