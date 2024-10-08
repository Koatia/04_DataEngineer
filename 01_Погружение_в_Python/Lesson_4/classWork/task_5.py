"""
Задание №5
Погружение в Python | Функции

✔ Функция принимает на вход три списка одинаковой длины:
✔ имена str,
✔ ставка int,
✔ премия str с указанием процентов вида «10.25%».
✔ Вернуть словарь с именем в качестве ключа и суммой
премии в качестве значения.
✔ Сумма рассчитывается как ставка умноженная на процент премии.
"""
import decimal

def func(names: list[str], salaries: list[int], awards: list[str]) -> dict[str, decimal.Decimal]:
    return {name: salary * decimal.Decimal(award.rstrip('%')) / 100 for name, salary, award in zip(names, salaries, awards)}

names = ['Борис', 'Иван', 'Петр', "Сергей"]
salaries = [10000, 12000, 16000, 14000]
awards = ['12.35%', '10.25%', '7.75%', '8.85%']

print(func(names, salaries, awards))
