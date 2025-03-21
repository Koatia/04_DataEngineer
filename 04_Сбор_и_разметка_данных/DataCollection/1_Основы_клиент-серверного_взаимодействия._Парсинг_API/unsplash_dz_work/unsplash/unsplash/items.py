# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UnsplashItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    categories = scrapy.Field()
    local_path = scrapy.Field()
    image_urls = scrapy.Field()
