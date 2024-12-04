# 2) Написать функцию, которая производит поиск и выводит на экран
# вакансии с заработной платой больше введенной суммы

from pymongo import MongoClient


def get_formatted_salary(min_val, max_val, curr_val):
    """Возвращает одной строкой красиво оформленную зарплату."""
    if curr_val is None:
        return 'не указана'
    elif min_val is None:
        return f'до {max_val} {curr_val}'
    elif max_val is None:
        return f'от {min_val} {curr_val}'
    else:
        return f'{min_val} - {max_val} {curr_val}'


# Подключение к базе данных MongoDB
client = MongoClient('localhost', 27017)
db = client['gb_db']
db_vacs = db.vacancies

# Печать информации о количестве вакансий в базе
count = db_vacs.count_documents({})
print(f'В базе данных {count} вакансий.')

# Получение информации о валютах из базы и создание уникального списка валют
currencies = set()
for cur in db_vacs.find({'salary_currency': {'$ne': None}}, {'_id': 0, 'salary_currency': 1}):
    currencies.add(cur['salary_currency'])
currencies = sorted(list(currencies))

print('Поиск вакансий по зарплате.')

# запрос минимальной зарплаты
while True:
    min_salary = input('- укажите желаемую зарплату (число): ')
    try:
        min_salary = int(min_salary)
    except ValueError:
        print('Ошибка. Введите число!')
    else:
        break

# запрос валюты
while True:
    print('- укажите валюту из списка:')
    for i, cur in enumerate(currencies, 1):
        print(f'  {i} - {cur}')
    currency = input(f'  введите число (1 - {len(currencies)}): ')
    try:
        currency = int(currency)
    except ValueError:
        print('Ошибка. Введите число!')
        continue
    if 1 <= currency <= len(currencies):
        currency = currencies[currency - 1]
        break

# вопрос про вакансии без зарплат
while True:
    print('- показывать вакансии без зарплаты?')
    print('  1 - показывать все вакансии')
    print('  2 - показывать только вакансии с зарплатой')
    salary_flag = input(f'  введите число (1 - 2): ')
    try:
        salary_flag = int(salary_flag)
    except ValueError:
        print('Ошибка. Введите число!')
        continue
    if 1 <= salary_flag <= 2:
        break

# Поиск в базе данных подходящих вакансий

if salary_flag == 1:
    # показывать все вакансии (с зарплатой и без)
    search_result = db_vacs.find({
        '$or': [
            {'salary_currency': None,  # зарплата вообще не указана
             'salary_min': None,
             'salary_max': None},
            {'salary_currency': currency,  # зарплата указана
             '$or': [
                 {'salary_max': {'$gte': min_salary}},  # в вакансии указана верхняя планка зарплаты
                 {'salary_max': None}  # в вакансии отсутствует верхняя планка зарплаты
             ]
             }
        ]
    })
else:
    # показывать только вакансии с зарплатой
    search_result = db_vacs.find({
        'salary_currency': currency,  # зарплата указана
        '$or': [
            {'salary_max': {'$gte': min_salary}},  # в вакансии указана верхняя планка зарплаты
            {'salary_max': None}  # в вакансии отсутствует верхняя планка зарплаты
        ]
    })

# Печать на экран списка найденных вакансий
for i, vac in enumerate(search_result, 1):
    print(f'{i}) {vac["title"]} ({vac["employer"]}, {vac["city"]})')
    print(f'Зарплата: {get_formatted_salary(vac["salary_min"], vac["salary_max"], vac["salary_currency"])}')
