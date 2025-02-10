# Установите MongoDB на локальной машине, а также зарегистрируйтесь в онлайн-сервисе. https://www.mongodb.com/ https://www.mongodb.com/products/compass
# Загрузите данные которые вы получили на предыдущем уроке путем скрейпинга сайта с помощью Buautiful Soup в MongoDB и создайте базу данных и коллекции для их хранения.
# Поэкспериментируйте с различными методами запросов.

# 1. Установка MongoDB в Docker (подключаемся к localhost:27017)
# docker run --name my-mongo -d -p 27017:27017 mongo
#
# 2. Для прямого подключения к контейнеру:
# docker exec -it my-mongo bash
# Теперь мы можем запустить в этом окружении mongosh для работы с системой, уже локально:
# mongosh


import json
from pymongo import MongoClient


# Подключение к серверу MongoDB
def connect_db():
    client = MongoClient('localhost', 27017)  # Это имя хоста получает контейнер, запускаемый Docker
    # Выбор базы данных и коллекции
    db = client.book_shop
    return db.books


# Чтение файла JSON
def load_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


# Функция разделения данных на более мелкие фрагменты
def chunk_data(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

    # Вставка фрагментов в коллекцию MongoDB


# Функция вставки фрагментов данных в db
def mongo_insert(book, data_chunks):
    books.delete_many({})  # Clear db

    for chunk in data_chunks:
        # books.insert_many(chunk)
        for book in chunk:
            _id = book.get('ref')
            book['_id'] = _id
            try:
                books.insert_one(book)
            except:
                print(book)
    print("Данные успешно вставлены.")


def example_mongo(collection):
    # Найдём общее количество документов
    book_count = collection.count_documents({})
    print(f'Число книг в базе данных: {book_count}')

    # Найдём книги, у которых цена более чем 50
    price_gte = collection.count_documents(filter={'price': {'$gte': 55.0}})
    print(f'Количество книг дороже 55.0: {price_gte}')

    # Найдём количество книг, которых на складе не более 15
    stock_lt = collection.count_documents(filter={'amount': {'$lt': 3}})
    print(f'Количество книг, которых на складе меньше 3: {stock_lt}')

    # Найдём книги, которые начинаются на букву 'F'
    projection = {'_id': 0, 'name': 1}
    books_starting_with_f = collection.find({'name': {'$regex': '^F', '$options': 'i'}}, projection)
    for book in books_starting_with_f:
        print(book)


if __name__ == "__main__":
    books = connect_db()
    data = load_json('all_books.json')

    # Разделение данных на фрагменты по 500 записей в каждом
    chunk_size = 500
    data_chunks = list(chunk_data(data, chunk_size))

    # mongo_insert(books, data_chunks)

    example_mongo(books)
