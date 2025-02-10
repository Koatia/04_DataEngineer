# Импортируем класс для создания процесса
from scrapy.crawler import CrawlerProcess

# Импортируем класс для настроек
from scrapy.settings import Settings

# Наши настройки
from bookparser import settings

# Классы наших пауков
from bookparser.spiders.labirint import LabirintSpider
from bookparser.spiders.book24 import Book24Spider


if __name__ == '__main__':
    # Создаем объект с настройками
    crawler_settings = Settings()

    # Привязываем к нашим настройкам
    crawler_settings.setmodule(settings)

    # Создаем объект процесса для работы
    process = CrawlerProcess(settings=crawler_settings)

    # Добавляем всех пауков
    process.crawl(LabirintSpider)
    process.crawl(Book24Spider)

    # Пуск
    process.start()
