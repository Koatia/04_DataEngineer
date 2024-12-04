# Загрузите данные которые вы получили на предыдущем уроке путем скрейпинга сайта с помощью Buautiful Soup в ClickHouse.
# Поэкспериментируйте с различными методами запросов.

# https://dockerhosting.ru/blog/clickhouse-v-docker/
# Запуск контейнера ClickHouse
# docker run -d -p 9000:9000 --name clickhouse-server clickhouse/clickhouse-server
#
# Проверка установки
# После запуска контейнера проверьте установку, войдя в клиент ClickHouse:
# docker exec -it clickhouse-server clickhouse-client
#
# Затем вы можете запускать базовые SQL-запросы, чтобы убедиться, что все настроено правильно:
# SELECT * FROM system.databases;
# В этом запросе перечислены все базы данных, доступные в ClickHouse.


import json
from clickhouse_driver import Client


# Подключение к серверу ClickHouse
def connect_db():
    client = Client(host='localhost')

    # Создание базы данных (если она не существует)
    client.execute('CREATE DATABASE IF NOT EXISTS book_shop')

    # Создание таблицы
    client.execute('''
    CREATE TABLE IF NOT EXISTS book_shop.books (
        name String,
        ref String,
        price Float64,
        amount Int64,
        description String
    ) ENGINE = MergeTree()
    ORDER BY ref
    ''')

    print("Таблица создана успешно.")
    return client


# Чтение файла JSON
def load_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


# Функция вставки данных в ClickHouse
def db_insert(client, data):
    # Преобразуем данные в формат списка кортежей
    rows = []
    for book in data:
        try:
            rows.append((
                book.get('name', ""),
                book.get('ref', ""),
                float(book.get('price', 0.0)),  # Преобразуем price в float
                int(book.get('amount', 0)),  # Преобразуем amount в int
                book.get('description', "")
            ))
        except (ValueError, TypeError) as e:
            print(f"Ошибка обработки данных книги {book}: {e}")

    # Батчевая вставка данных
    client.execute("""
        INSERT INTO book_shop.books (name, ref, price, amount, description) 
        VALUES
    """, rows)

    print("Данные успешно вставлены.")


def example_ClickHouse(client):
    # Запрос для подсчёта общего количества книг
    query = "SELECT COUNT(*) FROM book_shop.books"
    book_count = client.execute(query)[0][0]
    print(f'Число книг в базе данных: {book_count}')

    # Запрос для подсчёта книг с ценой более 55.0
    query = "SELECT COUNT(*) FROM book_shop.books WHERE price >= 55.0"
    price_gte = client.execute(query)[0][0]
    print(f'Количество книг дороже 55.0: {price_gte}')

    # Запрос для подсчёта книг, которых на складе меньше 3
    query = "SELECT COUNT(*) FROM book_shop.books WHERE amount < 3"
    stock_lt = client.execute(query)[0][0]
    print(f'Количество книг, которых на складе меньше 3: {stock_lt}')

    # Запрос для книг, название которых начинается с буквы 'F'
    query = """
    SELECT name 
    FROM book_shop.books 
    WHERE lower(name) LIKE 'f%' 
    """
    books_starting_with_f = client.execute(query)
    for book in books_starting_with_f:
        print(f"Название книги: {book[0]}")


if __name__ == "__main__":
    # Подключение к ClickHouse
    client = connect_db()

    # Загрузка данных из JSON
    data = load_json('all_books.json')

    # Вставка данных в ClickHouse
    # db_insert(client, data)

    example_ClickHouse(client)
