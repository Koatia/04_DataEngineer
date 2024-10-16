"""
Task 2.

Напишите функцию, принимающую на вход только ключевые параметры и возвращающую словарь,
где ключ — значение переданного аргумента, а значение — имя аргумента.
Если ключ не хешируем, используйте его строковое представление.
"""


def make_dict(**kwargs):
    """Функция принимает только ключевые параметры и возвращающую словарь,
    где ключ — значение переданного аргумента, а значение — имя аргумента"""

    print(dict(kwargs))
    new_dict = {}
    for key, value in kwargs.items():
        # Проверяем, если значение не является хэшируемым, преобразуем его в строку
        if isinstance(value, (list, dict, set)):
            value = str(value)
        new_dict[value] = key
    return new_dict


print(make_dict(size=12, fish=["Larry", "Curly", "Moe"], isExist=True))
