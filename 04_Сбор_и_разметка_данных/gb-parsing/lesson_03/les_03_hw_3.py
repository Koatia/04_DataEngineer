# 3*) Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта

from pymongo import MongoClient
import json

# Подключение к базе данных MongoDB
client = MongoClient('localhost', 27017)
db = client['gb_db']
db_vacs = db.vacancies

# Чтение вакансий из файла
# Беру вакансии из файла, а не с сайта, чтобы можно было
# в этом файле вручную экспериментировать (изменить, добавить, удалить)
output_filename = 'data_scientist_vacancies.json'
with open(output_filename, encoding='utf-8') as f:
    vacancies_data = json.load(f)

active_id_list = []
modified_count = 0
new_count = 0
# Проходимся по каждой вакансии и обновляем ее в базе
for vacancy in vacancies_data:
    vac_id = vacancy['id']
    # Обновление в базе имеющейся или добавление новой вакансии, если не было
    result = db_vacs.update_one(
        {'id': vac_id},
        {'$set': vacancy},
        upsert=True
    )
    # Счетчики обновлений и добавлений
    modified_count += result.modified_count
    if result.upserted_id is not None:
        new_count += 1
    # Собираем все действующие id
    active_id_list.append(vac_id)

# Если в базе нужно поддерживать только актуальные вакансии, а старые удалять,
# то удаляем вакансии, которых больше нет на сайте
result = db_vacs.delete_many({
    'id': {'$nin': active_id_list}
})
deleted_count = result.deleted_count

# Печать результатов обновления
print(f'Результат обновления базы данных:')
print(f'- записано новых вакансий: {new_count}')
print(f'- обновлено имеющихся вакансий: {modified_count}')
print(f'- удалено старых вакансий: {deleted_count}')
