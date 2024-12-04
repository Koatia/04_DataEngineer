# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

# Для подсказок объекта response
from scrapy.http import HtmlResponse

# Подключаем класс из items
from leroymerlin.items import LeroymerlinItem


class ProductSpider(scrapy.Spider):
    # Имя паука, разрешенные домены, стартовая страница
    name = 'product'
    allowed_domains = ['leroymerlin.ru']
    start_urls = []

    # Через конструктор передаем поисковую фразу
    def __init__(self, search=None):
        if search:
            self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    # С этого метода запускается парсинг страницы поиска
    def parse(self, response):
        # Цикл по всем товарам на текущей странице поиска
        product_links = response.xpath('//div[@class="product-name"]/a/@href').extract()
        for product_link in product_links:
            # Заходим на страницу товара и передаем парсинг в другой метод класса
            yield response.follow(product_link, callback=self.product_parse)

        # Ищем ссылку для перехода на следующую страницу
        next_page_ulr = response.xpath('//a[@class="paginator-button next-paginator-button"]/@href').extract_first()
        if next_page_ulr is not None:
            # Переходим по ссылке на следующую страницу, если она есть
            yield response.follow(next_page_ulr, callback=self.parse)

    # В этом методе обрабатываем страницу с одним товаром
    def product_parse(self, response: HtmlResponse):
        # Работаем через item loader
        loader = ItemLoader(item=LeroymerlinItem(), response=response)

        loader.add_value('url', response.url)
        loader.add_xpath('title', '//h1[@slot="title"]/text()')  # название
        loader.add_xpath('code', '//span[@slot="article"]/text()')  # артикул
        loader.add_xpath('price', '//span[@slot="price"]/text()')  # рубли
        loader.add_xpath('price', '//span[@slot="fract"]/text()')  # копейки

        # Спецификация товара (парсим все пары: параметр и значение)
        loader.add_xpath('specification', '//div[@class="def-list__group"]/dt/text() '
                                          '| //div[@class="def-list__group"]/dd/text()')

        # Фотографии товара
        loader.add_xpath('images', '//picture[@slot="pictures"]/source[4]/@data-origin')

        yield loader.load_item()
