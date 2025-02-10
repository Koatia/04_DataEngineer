"""
Задание 1

Создание из файла txt нового файла json
Имена пишите с большой буквы.
Каждую пару сохраняйте с новой строки.
"""

import json
import os
from pathlib import Path


def txt_to_json(file: str | Path) -> None:
    """Создание из созданного ранее файла нового с данными в формате JSON"""
    file = Path.cwd() / file
    if not os.path.isfile(file):
        print(f'Файл {file} не найден')
        return
    my_dict = {}
    with (open(file, 'r', encoding='utf-8') as f_in,  # открываем  файл .txt
          open(f'{file.stem}.json', "w", encoding='utf-8') as f_out):  # создаем .json
        contents = f_in.readlines()
        my_dict = {}
        for line in contents:  # данные из data.txt считываем в словарь my_dict
            name, number = line.split()
            my_dict[name.title()] = float(number)

        json.dump(my_dict, f_out, indent=2, ensure_ascii=False)  # запись в  .json словаря my_dict


if __name__ == '__main__':
    txt_to_json('task_3.txt')
