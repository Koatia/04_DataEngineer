# Импортируем класс для создания процесса
from scrapy.crawler import CrawlerProcess

# Импортируем класс для настроек
from scrapy.settings import Settings

# Наши настройки
from leroymerlin import settings

# Класс паука
from leroymerlin.spiders.product import ProductSpider


if __name__ == '__main__':
    # Создаем объект с настройками
    crawler_settings = Settings()

    # Привязываем к нашим настройкам
    crawler_settings.setmodule(settings)

    # Создаем объект процесса для работы
    process = CrawlerProcess(settings=crawler_settings)

    # Добавляем паука с поисковой фразой
    search_phrase = 'ведро'
    process.crawl(ProductSpider, search=search_phrase)

    # Пуск
    process.start()
