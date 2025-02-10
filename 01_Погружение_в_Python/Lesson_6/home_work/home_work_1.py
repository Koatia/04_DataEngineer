"""
В модуль с проверкой даты добавьте возможность запуска в терминале с передачей даты на проверку.

# Задача 7
#
# Создайте модуль и напишите в нём функцию, которая получает на вход дату в формате DD.MM.YYYY
# и возвращает истину, если дата может существовать или ложь,
# если такая дата невозможна. Для простоты договоримся, что год может быть в диапазоне [1, 9999].
# И весь период действует григорианский календарь.
# Проверку года на високосность вынести в отдельную защищённую функцию.
"""

from sys import argv


def _is_not_leap_year(year):
    return not (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))


def check_date(full_date: str) -> bool:
    day, month, year = (int(item) for item in full_date.split('.'))
    if year < 1 or year > 9999 or month < 1 or month > 12 or day < 1 or day > 31:
        return False
    if month in [4, 6, 9, 11] and day > 30:
        return False
    if month == 2 and day > 29:
        return False
    if month == 2 and _is_not_leap_year(year) and day > 28:
        return False
    else:
        return True


if __name__ == '__main__':
    print(check_date(argv[1]))
