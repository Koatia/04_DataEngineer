"""
Task 3.

Возьмите задачу о банкомате из семинара 2.
Разбейте её на отдельные операции — функции.
Дополнительно сохраняйте все операции поступления и снятия средств в список.

Напишите программу банкомат.
✔ Начальная сумма равна нулю
✔ Допустимые действия: пополнить, снять, выйти
✔ Сумма пополнения и снятия кратны 50 у.е.
✔ Процент за снятие — 1.5% от суммы снятия, но не менее 30 и не более 600 у.е.
✔ После каждой третей операции пополнения или снятия начисляются проценты - 3%
✔ Нельзя снять больше, чем на счёте
✔ При превышении суммы в 5 млн, вычитать налог на богатство 10%
   перед каждой операцией, даже ошибочной
✔ Любое действие выводит сумму денег
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
MIN_REMOVAL = decimal.Decimal(30)
MAX_REMOVAL = decimal.Decimal(600)
COUTER_OPER = 3

account = decimal.Decimal(0)
count: int = 0
list_operations: [decimal.Decimal] = []


def richness_pay(balance: decimal.Decimal, lst: [decimal.Decimal]) -> decimal.Decimal:
    """Функция расчета и удержания налога на богатство"""
    if balance > RICHNESS_SUM:
        sum_operation = balance * RICHNESS_TAX
        balance -= sum_operation
        lst.append(-sum_operation)
        print(f'С вас удержали налог на богатство {sum_operation:.2f} у.е.! '
              f'Баланс {balance:.2f} у.е.')
    return balance


def input_sum_operation() -> decimal.Decimal:
    """Функция ввода суммы операции"""
    sum_operation = decimal.Decimal(1)
    while sum_operation % MULTIPLIERS != 0 and sum_operation >= 0:
        sum_operation = decimal.Decimal(
            input(f"Введите сумму операции, кратную {MULTIPLIERS} у.е.: "))
    return sum_operation


def put_deposit(balance: decimal.Decimal, enum: int, lst: [decimal.Decimal]) \
        -> [decimal.Decimal, int]:
    """Функция пополнения счета"""
    sum_operation = input_sum_operation()
    balance += sum_operation
    lst.append(sum_operation)
    enum += 1
    print(f"Пополнение карты на {sum_operation:.2f} у.е. Баланс счета {balance:.2f} у.е.")
    return balance, enum


def get_deposit(balance: decimal.Decimal, enum: int, lst: [decimal.Decimal]) \
        -> [decimal.Decimal, int]:
    """Функция снятия наличных со счета"""
    sum_operation = input_sum_operation()
    withdraw_amount = sum_operation * WITHDRAW_PERCENTAGE

    if withdraw_amount > MAX_REMOVAL:
        withdraw_amount = MAX_REMOVAL
    elif withdraw_amount < MIN_REMOVAL:
        withdraw_amount = MIN_REMOVAL

    if withdraw_amount + sum_operation >= balance:
        print(
            f"Недостаточно средств для снятия {sum_operation:.2f} у.е. "
            f"и {withdraw_amount:.2f} у.е. платы за операцию")
        print(f"Баланс счета {balance:.2f} у.е.")
    else:
        balance -= sum_operation
        balance -= withdraw_amount
        lst.append(-sum_operation).append(-withdraw_amount)
        enum += 1
        print(f"Выдано {sum_operation:.2f} у.е. "
              f"Удержана плата за операцию {withdraw_amount:.2f} у.е.\n"
              f"Баланс счета {account:.2f} у.е.")
    return account, enum


def method_add_percentage(balance: decimal.Decimal, enum: int, lst: [decimal.Decimal]) \
        -> [decimal.Decimal, int]:
    """Метод начисления процентов за операции"""
    if enum == COUTER_OPER:
        sum_operation = balance * ADD_PERCENTAGE
        balance += sum_operation
        lst.append(sum_operation)
        enum = 0
        print(f'Вам начислено {sum_operation:.2f} у.е. за совершенные операции!'
              f' Баланс счета {balance:.2f} у.е.')
    return balance, enum


while True:
    command = input(f"Выберите операцию (Пополнить: {CMD_DEPOSIT},"
                    f" Снять: {CMD_WITHDRAW}, Выйти: {CMD_EXIT}): ")
    account = richness_pay(account, list_operations)

    if command == CMD_EXIT:
        print(f"Возьмите карту, на которой {account:.2f} у.е.")
        break

    if command == CMD_DEPOSIT:
        account, count = put_deposit(account, count, list_operations)
    elif command == CMD_WITHDRAW:
        account, count = get_deposit(account, count, list_operations)

    account, count = method_add_percentage(account, count, list_operations)
