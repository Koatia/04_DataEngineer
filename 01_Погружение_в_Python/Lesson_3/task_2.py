"""
Задача №2

Пользователь вводит данные. Сделайте проверку данных и преобразуйте, если возможно в один из вариантов ниже:
- целое положительное число,
- вещественное положительное или отрицательное число,
- строку в верхнем регистре, если в строке есть хотя бы одна заглавная буква,
- строку в нижнем регистре в остальных случаях.
"""

sentence = (input('Введите данные -> '))

if sentence.isdigit():
    sentence = int(sentence)
    res = "Введено целое положительное число: " + str(sentence)

elif sentence.count('.') == 1 and sentence.count('-') < 2 and sentence[1:].count('-') == 0 and \
        sentence.replace('.', '').replace('-', '').isdigit():
    sentence = float(sentence)
    res = "Введено вещественное положительное или отрицательное число: " + str(sentence)

elif not sentence.islower():
    sentence = sentence.upper()
    res = "Введена строка с заглавной буквой: " + str(sentence)

else:
    sentence = sentence.lower()
    res = "Введена строка строчными буквами: " + str(sentence)

print(res)
