"""
Task 3.

Возьмите задачу о банкомате из семинара 2.
Разбейте её на отдельные операции — функции.
Дополнительно сохраняйте все операции поступления и снятия средств в список.
"""
import decimal

CMD_DEPOSIT = "a"
CMD_WITHDRAW = "d"
CMD_EXIT = "e"
RICHNESS_SUM = decimal.Decimal(5_000_000)
RICHNESS_TAX = decimal.Decimal(0.1)
WITHDRAW_PERCENTAGE = decimal.Decimal(0.015)
ADD_PERCENTAGE = decimal.Decimal(0.03)
MULTIPLIERS = 50
MIN_REMOVAL = 30
MAX_REMOVAL = 600
COUTER_OPER = 3

account = decimal.Decimal(0)
count = 0

while True:
    command = input(f"Пополнить: {CMD_DEPOSIT}, Снять: {CMD_WITHDRAW}, Выйти: {CMD_EXIT}   ")

    if account > RICHNESS_SUM:
        account -= account * RICHNESS_TAX
        print(f'С вас сняли налог на богатство! Баланс {account:.2f} у.е.')

    if command == CMD_EXIT:
        print(f"Возьмите карту, на которой {account:.2f} у.е.")
        break

    if command in (CMD_DEPOSIT, CMD_WITHDRAW):
        ammount = 1
        while ammount % MULTIPLIERS != 0:
            ammount = int(input(f"Введите сумму операции, кратную {MULTIPLIERS}: "))

    if command == CMD_DEPOSIT:
        account += ammount
        count += 1
        print(f"Пополнение карты на {ammount:.2f} у.е. Баланс {account:.2f} у.е.")

    elif command == CMD_WITHDRAW:
        withdraw_ammount = ammount * WITHDRAW_PERCENTAGE
        if withdraw_ammount > MAX_REMOVAL:
            withdraw_ammount = MAX_REMOVAL
        elif withdraw_ammount < MIN_REMOVAL:
            withdraw_ammount = MIN_REMOVAL

        if withdraw_ammount + ammount >= account:
            print(f"Недостаточно средств для снятия {ammount:.2f} у.е. Баланс {account:.2f} у.е.")
        else:
            account -= withdraw_ammount
            account -= ammount
            count += 1
            print(f"Выдано {ammount:.2f} у.е. Баланс {account:.2f} у.е.")

    if count == COUTER_OPER:
        account += account * ADD_PERCENTAGE
        print(f'Вам начислен процент за операции! Баланс {account:.2f} у.е.')
        count = 0
