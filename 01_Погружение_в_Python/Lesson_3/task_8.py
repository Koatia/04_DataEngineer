"""
Задача №8

Три друга взяли вещи в поход. Сформируйте словарь, где ключ — имя друга, а значение — кортеж вещей. Ответьте на вопросы:
Какие вещи взяли все три друга.
Какие вещи уникальны, есть только у одного друга.
Какие вещи есть у всех друзей кроме одного и имя того, у кого данная вещь отсутствует.

Для решения используйте операции с множествами. Код должен расширяться
на любое большее количество друзей.
"""
hike = {'Андрей': ('спички', 'спальник', 'дрова', 'топор'),
        'Вася': ('спальник', 'спички', 'вода', 'еда'),
        'Катя': ('вода', 'спички', 'косметичка', 'топор')}

# Какие вещи взяли все три друга
allThings = set()
for things in hike.values():
    # for thing in set(things):
    #     allThings.add(thing)
    allThings.update(things)

print(f"Полный список вещей: {allThings}")

# Какие вещи уникальны, есть только у одного друга
uniqueThings = {}
for masterFriend, masterThings in hike.items():
    for slaveFriend, slaveThings in hike.items():
        if masterFriend != slaveFriend:
            if masterFriend not in uniqueThings:
                uniqueThings[masterFriend] = set(masterThings) - set(slaveThings)
            else:
                uniqueThings[masterFriend] -= set(slaveThings)
print(f"\nСписок уникальных вещей: {uniqueThings}")

# Какие вещи есть у всех друзей кроме одного и имя того, у кого данная вещь отсутствует
doubleThings = set(allThings)
for things in uniqueThings.values():
    doubleThings -= set(things)

print(f"\nСписок список дублирующихся вещей: {doubleThings}")

for friend, things in hike.items():
    print(f'У {friend} отсутствуют {doubleThings - set(things)}')
    print(f'Второй вариант: У {friend} отсутствуют {(set(things) ^ doubleThings) - set(uniqueThings[friend])}\n')
