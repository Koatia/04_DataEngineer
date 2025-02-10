import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = "hhru"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://nn.hh.ru/search/vacancy?area=66&professional_role=18"]

    def parse(self, response: HtmlResponse):

        links = response.xpath('//a[@data-qa="serp-item__title"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_pars)

        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_pars(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').get()
        salary = response.xpath('//div[@data-qa="vacancy-salary"]//text()').getall()
        url = response.url

        yield JobparserItem(name=name, salary=salary, url=url)
