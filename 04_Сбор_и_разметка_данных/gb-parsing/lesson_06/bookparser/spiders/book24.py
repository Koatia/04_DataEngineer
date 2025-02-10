# -*- coding: utf-8 -*-
import scrapy

# Для подсказок объекта response
from scrapy.http import HtmlResponse

# Подключаем класс из items
from bookparser.items import BookparserItem


class Book24Spider(scrapy.Spider):

    # Имя паука
    name = 'book24'

    # Домен, в котором разрешено работать пауку
    allowed_domains = ['book24.ru']

    # Стартовая страница
    # Фраза поиска книг: бизнес
    # Количество: около 1343 шт.
    start_urls = ['https://book24.ru/search/?q=%D0%B1%D0%B8%D0%B7%D0%BD%D0%B5%D1%81&available=1']

    # С этого метода запускается парсинг
    def parse(self, response: HtmlResponse):

        # Ищем на текущей странице ссылки на все книги (30 шт на полной странице)
        books_links = response.xpath('//a[@data-element="title"]/@href').extract()

        # Цикл по всем книгам
        for book_link in books_links:
            # Переходим на страницу книги и парсим информацию методом класса book_parse
            yield response.follow(book_link, callback=self.book_parse)

        # Ищем ссылку для перехода на следующую страницу
        next_page_ulr = response.xpath(
            '//a[@class="catalog-pagination__item _text js-pagination-catalog-item" '
            'and text()="Далее"]/@href'
        ).extract_first()
        if next_page_ulr is not None:
            # Переходим по ссылке на следующую страницу, если она есть
            yield response.follow(next_page_ulr, callback=self.parse)

    # В этом методе обрабатываем страницу с одной книгой.
    # Только парсинг, без обработки.
    def book_parse(self, response: HtmlResponse):

        # Получение url-а и парсинг информации о книжке
        book_url = response.url
        book_title = response.css('h1.item-detail__title::text').extract_first()
        book_authors = response.xpath('//div[@class="item-tab__chars-list"]/div[1]/span[2]/a/text()').extract()
        book_rating = response.css('span.rating__rate-value::text').extract_first()

        # Парсинг цены. Два разных тега
        price_normal = response.css('div.item-actions__price b::text').extract_first()
        price_old = response.css('div.item-actions__price-old::text').extract_first()

        # Возвращаем один item
        yield BookparserItem(url=book_url, title=book_title, authors=book_authors,
                             price_normal=price_normal, price_new=None, price_old=price_old,
                             rating=book_rating)
