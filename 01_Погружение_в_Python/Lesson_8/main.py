from pathlib import Path

from File_manager.create_file_json import set_users
from File_manager.create_file_txt import create_file_txt
from File_manager.csv_to_json import csv_to_json
from File_manager.csv_to_pickle import csv_to_pickle
from File_manager.directory_reference import directory_reference
from File_manager.json_to_csv import json_to_csv
from File_manager.json_to_pickle import json_to_pickle
from File_manager.pickle_to_csv import pickle_to_csv
from File_manager.txt_to_json import txt_to_json

if __name__ == '__main__':
    # Генерация нового текстового файла или добавление новых данных к существующему файлу
    create_file_txt('task_1.txt', 'w')
    for _ in range(10):
        create_file_txt('task_1.txt', 'a')

    # Создание из созданного ранее файла нового с данными в формате JSON
    txt_to_json('task_1.txt')

    # Ввод данных с клавиатуры и сохранение их в JSON файл
    set_users('users.json')

    # Сохраняет созданный в прошлом задании файл в формате CSV
    json_to_csv('users.json')

    # Запись из csv файла в json файл, где каждая строка csv файла представлена как отдельный json словарь
    csv_to_json('users.csv', 'new_users.json')

    # Ищет json файлы в указанной директории и сохраняет их содержимое в виде одноимённых pickle файлов
    json_to_pickle(Path.cwd())

    # Преобразует pickle файл, хранящий список словарей, в табличный csv файл
    pickle_to_csv('new_users.pickle')

    # Читает созданный csv файл без использования csv.DictReader. Распечатывает его как pickle строку.
    csv_to_pickle('new_users.csv')

    # Создает справочник по содержимому директории: (наименование объекта, тип объекта в директории, размер объекта,
    # родительская директория объекта)
    directory_reference(Path(Path.cwd()))
