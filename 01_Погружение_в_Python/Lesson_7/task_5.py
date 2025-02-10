"""
Задание №5
✔ Доработаем предыдущую задачу.
✔ Создайте новую функцию которая генерирует файлы с разными расширениями.
✔ Расширения и количество файлов функция принимает в качестве параметров.
✔ Количество переданных расширений может быть любым.
✔ Количество файлов для каждого расширения различно.
✔ Внутри используйте вызов функции из прошлой задачи.
"""

from random import randint, choices
from string import ascii_lowercase, digits


def create_file(extension: str, min_len: int = 6, max_len: int = 30,
                min_size: int = 256, max_size: int = 4096, count: int = 42) -> None:
    for _ in range(count):
        file_name = ''.join(choices(ascii_lowercase + digits + '_', k=randint(min_len, max_len))) + '.' + extension
        data = bytes(randint(0, 255) for _ in range(randint(min_size, max_size)))
        with open(file_name, 'wb') as f:
            f.write(data)


def generate_file(**kwargs) -> None:
    for extension, amount in kwargs.items():
        create_file(extension, count=amount)


if __name__ == '__main__':
    generate_file(bin=2, jpg=1, txt=3)
