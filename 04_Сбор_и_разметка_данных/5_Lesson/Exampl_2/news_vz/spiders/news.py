import scrapy
from scrapy.http import HtmlResponse
from news_vz.items import NewsVzItem


class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["fontanka.ru"]
    start_urls = ["https://www.fontanka.ru/"]

    def parse(self, response):
        links = response.xpath('//a[contains(@class, "text-style-ui-menu")]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.news_pars)

        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def news_pars(self, response: HtmlResponse):
        data = response.xpath('//time/@datetime').get()
        title = response.xpath('//h1[contains(@class, "title")]/text()').get()
        author = response.xpath('//div[@itemprop="name"]//text()').get()
        url = response.url

        yield NewsVzItem(data=data, title=title, author=author, url=url)
