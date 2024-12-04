import json
from pymongo import MongoClient

import requests

# Upload file
# response = requests.get("https://gbcdn.mrgcdn.ru/uploads/asset/5560965/attachment/357f7ccb20abaeedb8ccfda8e1045098.json")
# with open('crash-data.json','wb') as f:
#     f.write(response.content)


# Подключение к серверу MongoDB
client = MongoClient('localhost',27017)

# Выбор базы данных и коллекции
db = client['town_cary']
collection = db['crashes']

# Чтение файла JSON
with open('crash-data.json', 'r') as file:
    data = json.load(file)

data = data['features']

# Функция разделения данных на более мелкие фрагменты
def chunk_data(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

# Разделение данных на фрагменты по 5000 записей в каждом
chunk_size = 5000
data_chunks = list(chunk_data(data, chunk_size))

# Вставка фрагментов в коллекцию MongoDB
for chunk in data_chunks:
    collection.insert_many(chunk)

print("Данные успешно вставлены.")
