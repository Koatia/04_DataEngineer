"""
Напишите функцию, которая получает на вход директорию и рекурсивно
обходит её и все вложенные директории. Результаты обхода сохраните в
файлы json, csv и pickle.
○ Для дочерних объектов указывайте родительскую директорию.
○ Для каждого объекта укажите файл это или директория.
○ Для файлов сохраните его размер в байтах, а для директорий размер
файлов в ней с учётом всех вложенных файлов и директорий.
Соберите из созданных на уроке и в рамках домашнего задания функций
пакет для работы с файлами разных форматов.
"""

import csv
import json
import os
import pickle
from pathlib import Path


def dir_size(path='.') -> int:
    result = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                result += entry.stat().st_size
            elif entry.is_dir():
                result += dir_size(entry.path)
    return result


def get_size(path='.') -> int:
    if os.path.isfile(path):
        return os.path.getsize(path)
    elif os.path.isdir(path):
        return dir_size(path)


def directory_reference(directory: Path):
    data = {}
    fieldnames = ['object_name', 'path', 'object_size', 'object_type', 'parant_directory']
    rows = []

    with (open('result.json', 'w', encoding='utf-8') as f_json,
          open('result.csv', 'w', newline='', encoding='utf-8') as f_csv,
          open('result.pickle', 'wb') as f_pickle):

        for dir_path, dir_name, file_name in os.walk(directory):
            data.setdefault(dir_path, {})
            for dir_ in dir_name:
                size = get_size(dir_path + '/' + dir_)
                parent_dir = dir_path.split('\\')[-2] if len(dir_path.split('\\')) > 1 else ''
                data[dir_path].update(
                    {dir_: {'object_size': size, 'object_type': 'directory', 'parant_directory': parent_dir}})
                rows.append({'object_name': dir_, 'path': dir_path, 'object_size': size, 'object_type': 'directory',
                             'parant_directory': parent_dir})
            for i in file_name:
                size = get_size(dir_path + '/' + i)
                parent_dir = dir_path.split('\\')[-1] if len(dir_path.split('\\')) > 1 else ''
                data[dir_path].update(
                    {i: {'object_size': size, 'object_type': 'file', 'parant_directory': parent_dir}})
                rows.append({'object_name': i, 'path': dir_path, 'object_size': size, 'object_type': 'file',
                             'parant_directory': parent_dir})

        json.dump(data, f_json, indent=2)
        writer = csv.DictWriter(f_csv, fieldnames=fieldnames, dialect='excel-tab',
                                quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerows(rows)
        pickle.dump(data, f_pickle)
