# 1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# записывающую собранные вакансии в созданную БД

from pymongo import MongoClient
import json

# Подключение к базе данных MongoDB
client = MongoClient('localhost', 27017)
db = client['gb_db']
db_vacs = db.vacancies

# Чтение вакансий из файла
# Вакансии беру из файла, а не с сайта, чтобы не загромождать
# текущую учебную задачу парсингом сайта, который замет больше всего места.
# Парсер отдельным файлом прилагаю - почти копия домашки из предыдущего урока,
# добавил парсинг id вакансии с сайта
output_filename = 'data_scientist_vacancies.json'
with open(output_filename, encoding='utf-8') as f:
    vacancies_data = json.load(f)

# Очищаем коллекцию. Удаляем все элементы
db_vacs.delete_many({})

# Запись сразу всех вакансий (список словарей)
result = db_vacs.insert_many(vacancies_data)

# Печать результата
print(f'В базу данных записано {len(result.inserted_ids)} вакансий!')
