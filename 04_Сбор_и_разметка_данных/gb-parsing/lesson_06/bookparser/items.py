# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# Создаем структуру item-a
class BookparserItem(scrapy.Item):

    # Определяем все поля одного item-а, которые парсим со страницы книги
    url = scrapy.Field()  # Ссылка
    title = scrapy.Field()  # Название книги
    authors = scrapy.Field()  # Авторы
    price_normal = scrapy.Field()  # Обычная единственная цена
    price_new = scrapy.Field()  # Новая цена со скидкой
    price_old = scrapy.Field()  # Старая цена без скидки
    rating = scrapy.Field()  # Рейтинг
