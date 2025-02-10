# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from leroymerlin import settings
from pymongo import MongoClient
from os import path
import re

# Подключаем класс для контекстных подсказок
from leroymerlin.items import LeroymerlinItem


# В этом пайплайне сохраняем картинки
class ProductImagesPipeline(ImagesPipeline):

    # Загрузка фотографий
    def get_media_requests(self, item, info):
        if item['images']:
            for img in item['images']:
                try:
                    yield scrapy.Request(img, meta=item)
                except Exception as e:
                    print(e)

    # Изменение имени файла
    def file_path(self, request, response=None, info=None):
        # Формат папки (имя товара + артикул): vedro-dlya-musora-13-13745853
        # Имя файла (как в источнике): 13745853_02.jpg
        new_folder = re.search(r'product/([a-z0-9\-]+)-\d+/$', request.meta['url']).group(1)
        new_folder = f'{new_folder[:20]}-{request.meta["code"]}'
        file_name = request.url.rsplit('/', maxsplit=1)[1]
        new_path = path.join(new_folder, file_name)
        return new_path

    # Изменение информации о фотографиях
    def item_completed(self, results, item, info):
        if results:
            images_info = list()
            for ok, data in results:
                if ok:
                    # Оставляем только url и локальный путь до файла
                    images_info.append({
                        'url': data['url'],
                        'path': path.join(settings.IMAGES_STORE, data['path'])
                    })
            item['images'] = images_info
        return item


# В этом пайплайне сохраняем товар в базу данных
class DataBasePipeline:

    # В конструкторе открываем подключение к базе данных
    def __init__(self):

        # Подключаемся к базе и сохраняем подключение в классе
        self.mongodb_client = MongoClient('localhost', 27017)
        self.mongodb_collection = self.mongodb_client['gb_leroymerlin']['products']

        # Очищаем коллекцию от прежних товаров
        self.mongodb_collection.delete_many({})

    # В деструкторе закрываем подключение к базе данных
    def __del__(self):
        self.mongodb_client.close()

    # Обработчик товара
    def process_item(self, item: LeroymerlinItem, spider):

        # Запись книжки в базу
        self.mongodb_collection.insert_one(item)

        return item
