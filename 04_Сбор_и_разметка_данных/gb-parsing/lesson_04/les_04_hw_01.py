# 1) Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex.news
# Для парсинга использовать xpath. Структура данных должна содержать:
# - название источника,
# - наименование новости,
# - ссылку на новость,
# - дата публикации
# 2) Сложить все новости в БД

from lxml import html
from datetime import datetime as dt, timedelta
from pymongo import MongoClient
import requests
import re


def get_html_from_web(url, params=None):
    """
    Функция возвращает текст html-страницы по указанной ссылке.
    Если с сервера вернулась ошибка, то функция возвращает None.
    """

    # Заголовки Google Chrome
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.61 Safari/537.36',
        'Accept': '*/*'
    }

    # Запрос и ответ
    response = requests.get(url, params=params, headers=headers)

    # Если ответ сервера 200 Ок, то берем данные
    if response.ok:
        return response.text
    else:
        return None


def get_clear_text_from_list(text_in_list):
    """
    Очищает текст от непечатных символов. Текст на вход подается кусками в виде списка.
    """
    # Склеиваем список в строку
    clear_text = ''.join(text_in_list)

    # Заменяем непечатные символы на пробел
    clear_text = ''.join([s if s.isprintable() else ' ' for s in clear_text])

    return clear_text


def get_news_item_dict(title, url, date, source, portal):
    """
    Функция формирует словарь со всеми параметрами новости.
    """

    news_item = dict()

    news_item['title'] = title  # Заголовок новости
    news_item['url'] = url  # Ссылка на новость
    news_item['date'] = date  # Дата новости
    news_item['source'] = source  # Название новостного агентства
    news_item['portal'] = portal  # Новостной портал, с которого взяли новость

    return news_item


def get_news_params_from_mail_ru(url):
    """
    Функция загружает новость с сайта news.mail.ru, парсит html и возвращает ее параметры
    (дату выхода новости, источник новости)
    """

    # Загружаем страницу новости, чтобы получить дату и источник
    news_page_text = get_html_from_web(url)
    date = None
    source = None

    if news_page_text:

        # Создаем DOM страницы с конкретной новостью
        news_page_dom = html.fromstring(news_page_text)

        # Дата новости
        # Исходный вид на сайте: datetime = "2020-06-13T20:48:21+03:00"
        # Переводим в datetime, чтобы записать в базу данных
        date = news_page_dom.xpath('//span[@datetime]/@datetime')[0]
        date = dt.fromisoformat(date)

        # Источник новости
        source = news_page_dom.xpath('//a[contains(@class, "breadcrumbs__link")]'
                                     '/span[@class="link__text"]/text()')[0]

    return date, source


def get_news_from_mail_ru():
    """
    Функция возвращает ГЛАВНЫЕ НОВОСТИ ДНЯ с портала news.mail.ru.
    Собирается три блока новостей:
    - самая главная новость дня (1 шт. большая картинка);
    - четыре главные новости (4 шт. картинки);
    - текстовые новости (8 шт).
    Формат выдачи - список словарей.
    """

    # Получаем html
    base_url = 'https://news.mail.ru'
    html_text = get_html_from_web(base_url)

    # Список для хранения новостей
    news_data = []

    if html_text:

        # Создаем DOM новостной страницы
        dom = html.fromstring(html_text)

        # 1) ПАРСИНГ САМОЙ ГЛАВНОЙ НОВОСТИ ДНЯ (1 шт., большая картинка слева)

        # Заголовок новости + очистка
        title = dom.xpath('//div[contains(@class, "daynews__item_big")]'
                          '//span[contains(@class, "photo__title")]/text()')
        title = get_clear_text_from_list(title)

        # Ссылка на главную новость
        href = dom.xpath('//div[contains(@class, "daynews__item_big")]//a/@href')[0]
        href = base_url + href

        # Дату и источник загружаем со страницы конкретной новости
        date, source = get_news_params_from_mail_ru(href)

        # Собираем одну новость в словарь
        news_item = get_news_item_dict(title, href, date, source, 'news.mail.ru')

        # Добавляем новость в список
        news_data.append(news_item)

        # 2) ПАРСИНГ ГЛАВНЫХ НОВОСТЕЙ ДНЯ (4 шт., маленькие картинки справа)

        # Главные новости (с картинками, 4 шт.)
        pics_news = dom.xpath('//div[@class="daynews__item"]')

        # Цикл по четырем новостям
        for div in pics_news:

            # Заголовок новости + очистка
            title = div.xpath('.//span[contains(@class, "photo__title")]/text()')
            title = get_clear_text_from_list(title)

            # Ссылка на новость
            href = div.xpath('.//a/@href')[0]
            href = base_url + href

            # Дату и источник загружаем со страницы конкретной новости
            date, source = get_news_params_from_mail_ru(href)

            # Собираем одну новость в словарь
            news_item = get_news_item_dict(title, href, date, source, 'news.mail.ru')

            # Добавляем новость в список
            news_data.append(news_item)

        # 3) ПАРСИНГ ТЕКСТОВЫХ НОВОСТЕЙ ДНЯ (8 шт., текст под картинками)

        # Главные новости (текстовые, 8 шт.)
        text_news = dom.xpath(
            '//ul[@data-module = "TrackBlocks"]/li[@class="list__item"]'
            ' | //ul[@data-module = "TrackBlocks"]/li[@class="list__item hidden_small"]')

        # Цикл по текстовым новостям
        for li in text_news:

            # Заголовок новости + очистка
            title = get_clear_text_from_list(li.xpath('.//a/text()'))

            # Ссылка на новость
            href = li.xpath('.//a/@href')[0]

            if href.find('http') == -1:

                # Внутренняя сслыка на страницу news.mail.ru
                # Добавляем начало, чтобы получилась полная ссылка
                href = base_url + href

                # Дату и источник загружаем со страницы этой конкретной новости
                date, source = get_news_params_from_mail_ru(href)

            else:

                # Ссылка на какой-то внешний источник (ДА! ТАКОЕ БЫВАЕТ! ВИДЕЛ СВОИМИ ГЛАЗАМИ!)
                # Его не парсим, вырезаем название из ссылки
                source = re.findall(r'://(\w+\.?\w+\.\w+)/', href)
                source = source[0]

                # И вставляем сегодняшнюю дату
                now = dt.now()
                date = f'{now.day}.{now.month}.{now.year}'

            # Собираем одну новость в словарь
            news_item = get_news_item_dict(title, href, date, source, 'news.mail.ru')

            # Добавляем новость в список
            news_data.append(news_item)

    return news_data


def get_news_params_from_lenta_ru(url):
    """
    Функция загружает новость с сайта news.mail.ru, парсит html и возвращает ее параметры
    (дату выхода новости)
    """

    # Загружаем страницу новости, чтобы получить дату и источник
    news_page_text = get_html_from_web(url)
    date = None

    if news_page_text:

        # Создаем DOM страницы с конкретной новостью
        news_page_dom = html.fromstring(news_page_text)

        # Дата новости
        # Исходный вид на сайте: datetime="2020-06-12T14:06:00+03:00"
        # Переводим в datetime, чтобы записать в базу данных
        date = news_page_dom.xpath('//time[@pubdate]/@datetime')[0]
        date = dt.fromisoformat(date)

    return date


def get_news_from_lenta_ru():
    """
    Функция возвращает ГЛАВНЫЕ НОВОСТИ с портала lenta.ru
    Блок новостей находится в колонке справа (8 шт.)
    Формат выдачи - список словарей.
    """

    # Получаем html
    base_url = 'https://lenta.ru'
    html_text = get_html_from_web(base_url)

    # Список для хранения новостей
    news_data = []

    if html_text:

        # Создаем DOM новостной страницы
        dom = html.fromstring(html_text)

        # Главные новости (правая колонка, обычно 8-10 шт.)
        main_news = dom.xpath('//div[contains(@class, "b-yellow-box__wrap")]'
                              '//div[contains(@class, "item")]')

        # Цикл по новостям
        for div in main_news:

            # Заголовок новости + очистка
            title = div.xpath('.//a/text()')
            title = get_clear_text_from_list(title)

            # Ссылка на новость
            href = div.xpath('.//a/@href')[0]
            href = base_url + href

            # Дату и источник загружаем со страницы конкретной новости
            date = get_news_params_from_lenta_ru(href)

            # Собираем одну новость в словарь
            news_item = get_news_item_dict(title, href, date, 'Лента.Ру', 'lenta.ru')

            # Добавляем новость в список
            news_data.append(news_item)

    return news_data


def get_yandex_news_params(news_info):
    """
    Функция получает на вход массив строк с информацией о новости.
    Очищает текст, склеивает в одну строку, вырезает из этой строки
    и возвращает источник публикации и дату.
    """

    # Дата и источник новости, варианты строки на входе:
    # РИА Новости 19:50
    # Live24 вчера&nbsp;в&nbsp;20:14
    # Древние новости с указанием числа в главном блоке не появляются 

    # Очищаем и склеиваем в одну строку
    news_info_text = get_clear_text_from_list(news_info)

    # Разделяем источник и время выхода новости
    news_source, news_time = news_info_text.rsplit(sep=' ', maxsplit=1)

    if news_info_text.find('вчера') >= 0:
        # Вчерашняя новость. Берем вчерашнюю дату
        news_date = dt.now().date() - timedelta(days=1)
        # Вырезаем из источника "вчера в"
        news_source = news_source.replace(' вчера в', '')
    else:
        # Сегодняшняя новость. Берем сегодняшнюю дату
        news_date = dt.now().date()

    # Приводим к формату: "2020-06-12T14:06:00+03:00"
    news_date = dt.fromisoformat(f'{str(news_date)}T{news_time}:00+03:00')

    return news_source, news_date


def get_news_from_yandex_ru():
    """
    Функция возвращает ГЛАВНЫЕ НОВОСТИ с портала yandex.ru/news.
    В главные новости попадают разные разделы (Общество, Политика, Экономика..)
    Функция собирает три блока главных новостей:
    - самая главная новость (1 шт. большая картинка);
    - две главные новости (2 шт. маленькие картинки);
    - текстовые новости (2 шт).
    Формат выдачи - список словарей.
    """

    # Получаем html
    base_url = 'https://yandex.ru/news'
    html_text = get_html_from_web(base_url)

    # Список для хранения новостей
    news_data = []

    if html_text:

        # Создаем DOM новостной страницы
        dom = html.fromstring(html_text)

        # 1) ПАРСИНГ САМОЙ ГЛАВНОЙ НОВОСТИ ДНЯ (1 шт., большая картинка)

        # Заголовок новости + очистка
        title = dom.xpath('//div[@class="story__content"]'
                          '//a[contains(@class, "link_theme_black")]/text()')
        title = get_clear_text_from_list(title)

        # Ссылка на главную новость
        href = dom.xpath('//div[@class="story__content"]'
                         '//a[contains(@class, "link_theme_black")]//@href')[0]
        href = base_url + href

        # Дата и источник лежат вместе в одном теге
        # Разделяем их в функции
        news_info = dom.xpath('//div[@class="story__content"]'
                              '//div[@class="story__date"]/text()')
        source, date = get_yandex_news_params(news_info)

        # Собираем одну новость в словарь
        news_item = get_news_item_dict(title, href, date, source, 'yandex.ru/news')

        # Добавляем новость в список
        news_data.append(news_item)

        # 2) ПАРСИНГ ДВУХ ГЛАВНЫХ НОВОСТЕЙ (маленькие картинки слева)

        # Главные новости (с маленькими картинками, 2 шт.)
        two_pics_news = dom.xpath('//div[@class="story story_view_compact"]')

        # Цикл по двум новостям
        for div in two_pics_news:

            # Заголовок новости + очистка
            title = div.xpath('.//a[contains(@class, "link_theme_black")]/text()')
            title = get_clear_text_from_list(title)

            # Ссылка на новость
            href = div.xpath('.//a[contains(@class, "link_theme_black")]/@href')[0]
            href = base_url + href

            # Дата и источник лежат вместе в одном теге
            # Разделяем их в функции
            news_info = div.xpath('.//div[@class="story__date"]/text()')
            source, date = get_yandex_news_params(news_info)

            # Собираем одну новость в словарь
            news_item = get_news_item_dict(title, href, date, source, 'yandex.ru/news')

            # Добавляем новость в список
            news_data.append(news_item)

        # 3) ПАРСИНГ ДВУХ ТЕКСТОВЫХ НОВОСТЕЙ ДНЯ (правее двух новостей с маленькими картинками)

        # Текстовые новости (2 шт.)
        two_text_news = dom.xpath('//div[@class="story story_view_short"]')

        # Цикл по двум текстовым новостям
        for div in two_text_news:

            # Заголовок новости + очистка
            title = div.xpath('.//a[contains(@class, "link_theme_black")]/text()')
            title = get_clear_text_from_list(title)

            # Ссылка на новость
            href = div.xpath('.//a[contains(@class, "link_theme_black")]/@href')[0]
            href = base_url + href

            # Дата и источник лежат вместе в одном теге
            # Разделяем их в функции
            news_info = div.xpath('.//div[@class="story__date"]/text()')
            source, date = get_yandex_news_params(news_info)

            # Собираем одну новость в словарь
            news_item = get_news_item_dict(title, href, date, source, 'yandex.ru/news')

            # Добавляем новость в список
            news_data.append(news_item)

    return news_data


# ######### #
# ПРОГРАММА #
# ######### #

# Список для хранения всех новостей со всех новостных порталов
all_news = []

# Добавляем новости с news.mail.ru
mail_news = get_news_from_mail_ru()
all_news.extend(mail_news)

# Добавляем новости с lenta.ru
lenta_news = get_news_from_lenta_ru()
all_news.extend(lenta_news)

# Добавляем новости с yandex.ru/news
yandex_news = get_news_from_yandex_ru()
all_news.extend(yandex_news)

# ЗАПИСЬ ВСЕХ СОБРАННЫХ ВАКАНСИЙ В БАЗУ ДАННЫХ

# Подключение к базе данных MongoDB
client = MongoClient('localhost', 27017)
db = client['gb_news']
db_news = db.news

# Очищаем коллекцию. Удаляем все элементы
db_news.delete_many({})

# Запись сразу всех новостей со всех порталов (список словарей)
result = db_news.insert_many(all_news)

# Печать результата
print(f'Скрапинг трех порталов завершен.')
print(f'В базу данных записано {len(result.inserted_ids)} новостей.')
print(f'- {len(mail_news)} шт. с портала news.mail.ru')
print(f'- {len(lenta_news)} шт. с портала lenta.ru')
print(f'- {len(yandex_news)} шт. с портала yandex.ru/news')
