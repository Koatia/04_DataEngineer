# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv

class NewsVzPipeline:
    def __init__(self):
        self.file = None
        self.writer = None

    def open_spider(self, spider):
        # Метод вызывается при старте паука
        filename = f"{spider.name}.csv"
        self.file = open(filename, 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['data', 'title', 'author', 'url'])  # Заголовки CSV

    def process_item(self, item, spider):
        # Обработка каждого item
        self.writer.writerow([
            item.get('data', ''),
            item.get('title', ''),
            item.get('author', ''),
            item.get('url', '')
        ])
        return item

    def close_spider(self, spider):
        # Метод вызывается при завершении работы паука
        if self.file:
            self.file.close()