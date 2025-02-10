"""
Задача №6

Пользователь вводит строку текста. Вывести каждое слово с новой строки. Строки нумеруются начиная с единицы.
Слова выводятся отсортированными, согласно кодировки Unicode. Текст выравнивается по правому краю так,
чтобы у самого длинного слова был один пробел между ним и номером строки.
"""
# sentence = str(input('Тут строка текста -->>> '))
sentence = "чтобы у самого длинного слова был один пробел между ним и номером строки"

myList = sentence.split(' ')
myList.sort()
lenMaxPos = len(str(len(myList)))

maxLen = 0
for item in myList:
    if len(item) > maxLen:
        maxLen = len(item)

print(lenMaxPos, maxLen)

for pos, item in enumerate(myList):
    print(f'{pos:<{lenMaxPos}}  {item:>{maxLen}}')
