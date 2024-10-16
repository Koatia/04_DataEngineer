"""
Напишите функцию, которая принимает на вход строку — абсолютный путь до файла.
Функция возвращает кортеж из трёх элементов: путь, имя файла, расширение файла.
"""
import os


def file_info(file_path: str) -> (str, str, str):
    """
    Функция возвращает кортеж из трёх элементов: путь, имя файла, расширение файла
    :param file_path: абсолютный путь до файла
    :return:
    """
    path, filename = os.path.split(file_path)
    name, extension = os.path.splitext(filename)
    return path, name, extension


print(file_info('/Lesson_5/home_work/home_work_1.py'))
