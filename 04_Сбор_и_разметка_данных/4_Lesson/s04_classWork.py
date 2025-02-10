from lxml import html
import requests

url = 'https://www.kolesa.ru/article'

response = requests.get(url, headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
tree = html.fromstring(response.content)

names = tree.xpath('//span[@class="post-name"]/text()')
descriptions = tree.xpath('//span[@class="post-lead"]/text()')
dates = tree.xpath('//span[@class="post-meta-item pull-right"]/text()')
links = tree.xpath('//a[@class="post-list-item"]/@href')
print()
