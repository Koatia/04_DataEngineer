"""
Задача 6

Добавьте в модуль с загадками функцию, которая принимает на вход строку (текст загадки)
 и число (номер попытки, с которой она угадана).
Функция формирует словарь с информацией о результатах отгадывания.
 Для хранения используйте защищённый словарь уровня модуля.
Отдельно напишите функцию, которая выводит результаты угадывания из защищённого словаря
 в удобном для чтения виде.
Для формирования результатов используйте генераторное выражение.
"""
__all__ = ['riddle', 'storage', 'show_results', 'save_result']
_data = {}


def riddle(riddle_txt: str, ansvers: list[str], count: int = 3) -> int:
    """from task 4"""
    print(f"Отгадай загадку:\n{riddle_txt}")

    for nn in range(1, count + 1):
        ans = input(f"Попытка №{nn}: ").lower()
        if ans in ansvers:
            return nn
    return 0


def save_result(puzzle: str, nn: int) -> None:
    _data[puzzle] = nn


def show_results() -> None:
    res = (f"Загадку '{puzzle}' разгадали с {nn}-й попытки" if nn > 0
           else f"Загадку '{puzzle}' не разгадали"
           for puzzle, nn in _data.items())
    print(*res, sep="\n")


def storage():
    puzzels = {"Зимой и летом одним цветом?": ["ель", "ёлка", "елка", "сосна"],
               "Сидит дед во сто шуб одет?": ["лук", "луковица"],
               "Не лает, не кусает а в дом не пускает?": ["замок", "домофон"]}
    for puzzle, answer in puzzels.items():
        result = riddle(puzzle, answer)
        print(f"Угадал c {result}-й попытки!!!" if result > 0 else 'Не угадал...')
        save_result(puzzle, result)


if __name__ == '__main__':
    storage()
    show_results()
