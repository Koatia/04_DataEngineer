import csv
from lxml import html
import requests
from pprint import pprint

# URL страницы
url = 'https://www.kolesa.ru/article?page=1'

# Запрос к странице с заголовком User-Agent
response = requests.get(url, headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})

# Парсинг HTML-структуры
tree = html.fromstring(response.text)

# Поиск элементов статей
items = tree.xpath('//a[@class="post-list-item"]')
items_list = []

# Обработка каждого элемента статьи
for item in items:
    # Инициализация словаря для хранения данных статьи
    item_dict = {}

    # Извлечение данных
    title = item.xpath('.//span[@class="post-name"]/text()')
    description = item.xpath('.//span[@class="post-lead"]/text()')
    date = item.xpath('.//span[@class="post-meta-item pull-right"]/text()')
    link = item.xpath('./@href')

    # Очистка данных
    item_dict['title'] = title[0].strip() if title else 'Нет заголовка'
    item_dict['description'] = description[0].strip() if description else 'Нет описания'
    item_dict['date'] = date[0].strip().replace('\n', '').strip() if date else 'Нет даты'
    item_dict['link'] = link[0].strip() if link else 'Нет ссылки'

    # Добавление статьи в список, если есть заголовок
    if item_dict['title'] != 'Нет заголовка':
        items_list.append(item_dict)

# Вывод результатов для проверки
pprint(items_list)

# Запись данных в CSV
with open('articles.csv', 'w', encoding='utf-8', newline='') as csvfile:
    # Определение названий столбцов
    fieldnames = ["title", "description", "date", "link"]

    # Создание writer и запись заголовков
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Запись строк
    writer.writerows(items_list)

print("Данные успешно записаны в файл articles.csv")
