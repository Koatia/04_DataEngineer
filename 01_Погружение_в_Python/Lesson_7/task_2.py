"""
Напишите функцию, которая генерирует псевдоимена.
Имя должно начинаться с заглавной буквы, состоять из 4-7 букв, среди которых обязательно должны быть гласные.
Полученные имена сохраните в файл.
"""

from random import randint, choice
from pathlib import Path

VOWELS = 'eyuioa'
CONSONANTS = 'qwrtpsdfghjklzxcvbnm'
MIN_LEN = 2
MAX_LEN = 7


def make_random_name(filename: str | Path, count: int) -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        for _ in range(count):
            name = ''
            cur_vowel = randint(-1, 1)
            for i in range(randint(MIN_LEN, MAX_LEN)):
                if cur_vowel < 0:
                    name += choice(VOWELS)
                else:
                    name += choice(CONSONANTS)
                cur_vowel *= -1
            print(name.title(), file=f)


if __name__ == '__main__':
    make_random_name('task_2.txt', 120)
