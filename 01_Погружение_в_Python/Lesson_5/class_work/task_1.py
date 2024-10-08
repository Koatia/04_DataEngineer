"""
Задание 1

Пользователь вводит строку из четырёх или более целых чисел, разделённых символом “/”.
Сформируйте словарь, где:
- второе и третье число являются ключами.
- первое число является значением для первого ключа.
- четвертое и все возможные последующие числа хранятся в кортеже как значения второго ключа
"""

def dict_with_int(text_string: str) -> dict[int:int]:
    first, second, third, *another = (int(i) for i in text_string.split("/"))
    return {second: first, third: tuple(map(int, another))}

text = "3/6/8/5/4/3/9"
print(dict_with_int(text))
