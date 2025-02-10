# Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ и извлечь информацию о всех книгах на сайте
# во всех категориях: название, цену, количество товара в наличии (In stock (19 available)) в формате integer, описание.
#
# Затем сохранить эту информацию в JSON-файле.

# https://books.toscrape.com/catalogue/page-2.html

import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'http://books.toscrape.com/catalogue/'
START_PAGE = 'page-1.html'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

session = requests.Session()  # Используем сессию для повторного использования соединений
all_books = []


def parse_book_details(book_url):
    """
    Получить детали книги с её страницы (количество на складе и описание).
    """
    response = session.get(book_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Ошибка загрузки страницы книги: {book_url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        # Извлечение количества
        amount_str = soup.find('p', {'class': 'instock availability'}).getText().strip()
        amount = int(''.join(filter(str.isdigit, amount_str)))  # Убираем все символы кроме цифр и преобразуем в число

        # Извлечение описания из meta-тэга (атрибут content)
        description_tag = soup.find('meta', {'name': 'description'})
        description = description_tag['content'].strip() if description_tag else "Описание отсутствует"

    except Exception as e:
        print(f"Ошибка извлечения данных книги {book_url}: {e}")
        return None

    return {'amount': amount, 'description': description}


def scrape_page(page_url):
    """
    Извлечь информацию о книгах с одной страницы списка.
    """
    response = session.get(page_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Ошибка загрузки страницы: {page_url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', {'class': 'product_pod'})

    page_books = []
    for book in books:
        try:
            # Название книги и ссылка
            name_info = book.find('h3').find('a')
            name = name_info.getText().strip()
            ref = BASE_URL + name_info.get('href')

            # Цена
            price_str = book.find('div', {'class': 'product_price'}).find('p', {'class': 'price_color'}).getText()
            price = float(price_str[2:])  # Убираем символ валюты (£), конвертируем в число

            # Получаем детали книги
            details = parse_book_details(ref)
            if details is None:
                continue

            # Собираем данные о книге
            book_info = {
                'name': name,
                'ref': ref,
                'price': price,
                'amount': details['amount'],
                'description': details['description']
            }
            page_books.append(book_info)
        except Exception as e:
            print(f"Ошибка обработки книги: {e}")

    return page_books


def scrape_all_books():
    """
    Сбор данных о всех книгах, переходя по страницам.
    """
    next_page = START_PAGE
    while next_page:
        print(f"Обработка страницы: {next_page}")
        page_url = BASE_URL + next_page
        page_books = scrape_page(page_url)
        all_books.extend(page_books)

        # Находим ссылку на следующую страницу
        try:
            response = session.get(page_url, headers=HEADERS)
            soup = BeautifulSoup(response.text, 'html.parser')
            next_page = soup.find('li', {'class': 'next'}).find('a')['href']
        except AttributeError:
            next_page = None  # Если следующей страницы нет, выходим из цикла

    print(f"Всего книг собрано: {len(all_books)}")


if __name__ == "__main__":
    scrape_all_books()

    # Сохранение в JSON
    with open('all_books.json', 'w', encoding='utf-8') as fp:
        json.dump(all_books, fp, ensure_ascii=False, indent=4)
