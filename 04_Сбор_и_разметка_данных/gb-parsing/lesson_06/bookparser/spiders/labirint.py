# -*- coding: utf-8 -*-
import scrapy

# Для подсказок объекта response
from scrapy.http import HtmlResponse

# Подключаем класс из items
from bookparser.items import BookparserItem


class LabirintSpider(scrapy.Spider):

    # Имя паука
    name = 'labirint'

    # Домен, в котором разрешено работать пауку
    allowed_domains = ['labirint.ru']

    # Стартовая страница
    # Фраза поиска книг: фантастика
    # Количество: около 1000 шт.
    start_urls = ['https://www.labirint.ru/search/%D1%84%D0%B0%D0%BD%D1%82%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%B0/?stype=0']

    # С этого метода запускается парсинг
    def parse(self, response: HtmlResponse):

        # Ищем на текущей странице ссылки на все книги (60 шт на полной странице)
        books_links = response.css('a.product-title-link::attr(href)').extract()

        # Цикл по всем книгам
        for book_link in books_links:

            # Переходим на страницу книги и парсим информацию методом класса book_parse
            yield response.follow(book_link, callback=self.book_parse)

        # Ищем ссылку для перехода на следующую страницу
        next_page_ulr = response.css('a.pagination-next__text::attr(href)').extract_first()
        if next_page_ulr is not None:
            # Переходим по ссылке на следующую страницу, если она есть
            yield response.follow(next_page_ulr, callback=self.parse)

    # В этом методе обрабатываем страницу с одной книгой.
    # Только парсинг, без обработки.
    def book_parse(self, response: HtmlResponse):

        # Получение url-а и парсинг информации о книжке
        book_url = response.url
        book_title = response.xpath('//div[@id="product-title"]/h1/text()').extract_first()
        book_authors = response.xpath('//div[@class="authors"]/a[@data-event-label="author"]/text()').extract()
        book_rating = response.xpath('//div[@id="rate"]/text()').extract_first()

        # Парсинг цены. Три разных тега.
        price_normal = response.css('span.buying-price-val-number::text').extract_first()
        price_new = response.css('span.buying-pricenew-val-number::text').extract_first()
        price_old = response.css('span.buying-priceold-val-number::text').extract_first()

        # Возвращаем один item
        yield BookparserItem(url=book_url, title=book_title, authors=book_authors,
                             price_normal=price_normal, price_new=price_new, price_old=price_old,
                             rating=book_rating)
