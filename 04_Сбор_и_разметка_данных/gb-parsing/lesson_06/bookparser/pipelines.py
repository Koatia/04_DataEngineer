# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

# Подключаем класс для контекстных подсказок
from bookparser.items import BookparserItem


# Класс для обработки item-а
class BookparserPipeline:

    # В конструкторе открываем подключение к базе данных
    def __init__(self):
        # Подключаемся к базе и сохраняем подключение в классе
        self.mongodb_client = MongoClient('localhost', 27017)
        self.mongodb_base = self.mongodb_client['gb_books']

        # Очищаем коллекцию от прежних книг
        self.mongodb_base['labirint'].delete_many({})
        self.mongodb_base['book24'].delete_many({})

    # В деструкторе закрываем подключение к базе данных
    def __del__(self):
        self.mongodb_client.close()

    # Здесь идет обработка данных после парсинга и запись в базу данных
    def process_item(self, item: BookparserItem, spider):

        # Выбираем коллекцию для сохранения item-а по имени паука
        mongobd_collection = self.mongodb_base[spider.name]

        # Для записи цен. Они по-разному собираются с двух сайтов
        book_price = None
        book_discount_price = None

        # Какой паук принес книжку?
        if spider.name == 'labirint':

            # Книжка поступила с сайта labirint.ru

            # Отрезаем авторов из названия книги. Журналы идут без авторов
            book_title_list = str(item['title']).split(': ', maxsplit=1)
            if len(book_title_list) == 2:
                item['title'] = book_title_list[1]

            # Парсинг цены. Всего два варианта:
            # - одна цена
            # - две цены (новая со скидкой и старая базовая)
            # На сайте парсим три варианта тегов, все три передаем через item, здесь обрабатываем
            if item['price_normal']:
                # На сайте указана одна цена
                try:
                    book_price = int(item['price_normal'])
                except ValueError:
                    book_price = None
                finally:
                    item['price_normal'] = book_price
            else:
                # На сайте указаны две цены (обычная и со скидкой)
                try:
                    book_price = int(item['price_old'])
                    book_discount_price = int(item['price_new'])
                except ValueError:
                    book_price = None
                    book_discount_price = None
                finally:
                    item['price_old'] = book_price
                    item['price_new'] = book_discount_price

            # Преобразование рейтинга
            try:
                item['rating'] = float(item['rating'])
            except ValueError:
                item['rating'] = None

        elif spider.name == 'book24':

            # Книжка поступила с сайта book24.ru

            # Парсинг цены. Всего два варианта:
            # - одна цена
            # - две цены (цена со скидкой и старая базовая цена)
            if item['price_old']:
                # На сайте указаны две цены (новая со скидкой и старая)
                try:
                    book_price = int(self.get_clear_price(item['price_old']))
                    book_discount_price = int(self.get_clear_price(item['price_normal']))
                except ValueError:
                    book_price = None
                    book_discount_price = None
                finally:
                    item['price_old'] = book_price
                    item['price_normal'] = book_discount_price
            else:
                # На сайте указана только одна цена
                try:
                    book_price = int(self.get_clear_price(item['price_normal']))
                except ValueError:
                    book_price = None
                finally:
                    item['price_normal'] = book_price

            # Преобразование рейтинга
            try:
                item['rating'] = float(str(item['rating']).replace(',', '.'))
            except ValueError:
                item['rating'] = None

        # Запись книжки в базу
        mongobd_collection.insert_one(self.get_book_item_for_db(
            url=item['url'],
            title=item['title'],
            authors=item['authors'],
            price=book_price,
            discount_price=book_discount_price,
            rating=item['rating']
        ))

        return item

    @staticmethod
    def get_book_item_for_db(url, title, authors, price, discount_price, rating):
        """Метод формирует словарь с информацией об одной книге для записи в базу данных."""
        return {
            'url': url,
            'title': title,
            'authors': authors,
            'price': price,
            'discount_price': discount_price,
            'rating': rating
        }

    @staticmethod
    def get_clear_price(price: str):
        """Функция возвращает цену без рублей и пробелов"""
        return price.replace('р.', '').replace(' ', '')
