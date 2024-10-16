"""
Создайте модуль с функцией внутри.

Функция получает на вход загадку, список с возможными вариантами отгадок и количество попыток на угадывание.
Программа возвращает номер попытки, с которой была отгадана загадка или ноль, если попытки исчерпаны.
"""


def riddle(riddle_txt: str, ansvers: list[str], count: int = 3) -> int:
    print(f"Отгадай загадку:\n{riddle_txt}")

    for nn in range(1, count + 1):
        ans = input(f"Попытка №{nn}: ").lower()
        if ans in ansvers:
            return nn
    return 0


if __name__ == '__main__':
    result = riddle("Зимой и летом одним цветом?", ["Ель", "Ёлка", "елка", "сосна"])
    print(f"Угадал c {result}й попытки!!!" if result > 0 else 'Не угадал...')
