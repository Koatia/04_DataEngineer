# 2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo
# и складывает данные в БД. Магазины можно выбрать свои.
# Главный критерий выбора: динамически загружаемые товары

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import time


def get_hit_item(title, url, price):
    """Функция возвращает словарь с одним товаром-хитом."""
    return {
        'title': title,
        'url': url,
        'price': price
    }


def prepare_text_to_number_conversion(num_in_text):
    """Очищает текст от непечатных символов, чтобы можно было сконвертировать в число."""

    # Заменяем непечатные символы на пробел
    clear_text = ''.join([s if s.isprintable() else '' for s in num_in_text])
    clear_text = clear_text.replace(' ', '')
    clear_text = clear_text[0:-1]

    return clear_text


# Список для сбора товаров
all_bestsellers = list()

# Настройка параметров браузера (на весь экран)
chrome_options = Options()
chrome_options.add_argument('start-maximized')

# Создаем драйвер с параметрами браузера
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)

# Загружаем страницу
driver.get('https://www.mvideo.ru')

# Проверка страницы
assert "М.Видео" in driver.title

# Листаем страницу вниз до блока "Хиты продаж"
# и еще немного прокручиваем, чтобы увидеть хиты и прокрутку товаров
# в ходе исполнения программы
time.sleep(5)
title_tags = driver.find_elements_by_class_name('gallery-title-wrapper')
for title_tag in title_tags:
    if 'Хиты продаж' in title_tag.text:
        actions = ActionChains(driver)
        actions.move_to_element(title_tag)
        actions.perform()
        driver.execute_script(f'window.scrollBy(0, 600)')

# В цикле собираем каждую партию товаров-хитов
# Всего 16 товаров (4 страницы/прокрутки)
for page_num in range(1, 5):

    # Подождем загрузки, чтобы глазами увидеть смену картинок
    time.sleep(3)

    # Собираем информацию о четырех товарах
    ul_tags = driver.find_elements_by_xpath('//ul[@class="accessories-product-list"]')
    for ind, ul_tag in enumerate(ul_tags, 1):
        # Наши товары-хиты лежат третьем ul-е
        if ind == 3:
            titles = []
            urls = []
            prices = []
            # Собираем названия и ссылки
            a_tags = ul_tag.find_elements_by_class_name('sel-product-tile-title')
            for cnt, a_tag in enumerate(a_tags, 1):
                titles.append(a_tag.text)
                urls.append(a_tag.get_attribute('href'))
                if cnt == 4:
                    break
            # Собираем цены
            div_tags = ul_tag.find_elements_by_class_name('c-pdp-price__current')
            for cnt, div_tag in enumerate(div_tags, 1):
                prices.append(float(prepare_text_to_number_conversion(div_tag.text)))
                if cnt == 4:
                    break
            # Добавляем четыре товара в общий список
            for i in range(4):
                all_bestsellers.append(get_hit_item(titles[i], urls[i], prices[i]))
            break

    # Переключение на следующую страницу товаров через карусель
    carousel_divs = driver.find_elements_by_class_name('carousel-paging')
    for i, carousel_div in enumerate(carousel_divs, 1):
        # Наша карусель - четвертая
        if i == 4:
            # Цикл по ссылкам на страницы/прокрутки
            a_tags = carousel_div.find_elements_by_xpath('.//a')
            for j, a_tag in enumerate(a_tags, 1):
                if j == page_num + 1:
                    a_tag.click()
                    break
            break

# Закрываем Selenium
driver.quit()

# ЗАПИСЬ ВСЕХ СОБРАННЫХ ТОВАРОВ-БЕСТСЕЛЛЕРОВ В БАЗУ ДАННЫХ

# Подключение к базе данных MongoDB
client = MongoClient('localhost', 27017)
db = client['gb_mvideo']
db_bestsellers = db.bestsellers

# Очищаем коллекцию. Удаляем все элементы
db_bestsellers.delete_many({})

# Запись сразу всех товаров (список словарей)
result = db_bestsellers.insert_many(all_bestsellers)

# Печать результата
print(f'Скрапинг товаров-бестселлеров на М.Видео завершен.')
print(f'В базу данных записано {len(result.inserted_ids)} товаров.')
