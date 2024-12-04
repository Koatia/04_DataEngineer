# Установка пакетов
# !pip install selenium
# !pip install pandas
# !pip install matplotlib
# !pip install pymongo

# %%
import re
import time

import matplotlib.pyplot as plt
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Настройка формата вывода чисел float
pd.set_option('display.float_format', '{:.2f}'.format)

# %%
options = Options()
options.add_argument("--disable-notifications")
# Запуск браузера с развернутым экраном
options.add_argument('start-maximized')
# Будем использовать браузер Chrom
driver = webdriver.Chrome(options=options)
# Открываем ссылку
driver.get('https://www.wildberries.ru/')
time.sleep(4)

# %%
wait = WebDriverWait(driver, 10)
# Ищем строку поиска
# input = driver.find_element(By.XPATH, "//input[@id='searchInput']")
input = wait.until(EC.presence_of_element_located((By.ID, "searchInput")))
# Вводим фразу поиска и нажимаем Enter
input.send_keys('калоши утепленные мужские 45')
input.send_keys(Keys.ENTER)

# %%
# Прокручиваем страницу и записываем все ссылки на товары, если есть кнопка "далее" - нажимаем её, если нет - выходим из цикла
# Список ссылок на страницы товара
url_list = []

while True:
    # Кол-во товаров на странице
    count = None
    while True:
        time.sleep(4)
        # Ожидание появление объекта ((html код) карточек товара)
        cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//article[@id]')))
        # Выходим из цикла, если при прокрутке страницы, количество товаров не меняется
        if len(cards) == count:
            break
            # Вычисление кол-ва карточек товара на странице
        count = len(cards)

        # Прокручиваем страницу выполняя JAVA Script
        driver.execute_script('window.scrollBy(0, 1800)')
        time.sleep(2)

    # Сбор ссылок на товары с полностью загруженной страницы
    for card in cards:
        # Записываем ссылку каждого товара
        url = card.find_element(By.XPATH, './div/a').get_attribute('href')
        url_list.append(url)

    # Проверка кнопки "Следующая страница"
    try:
        next = driver.find_element(By.XPATH, "//a[@class='pagination-next   pagination__next j-next-page']")
        actions = ActionChains(driver)
        actions.move_to_element(next).click()
        actions.perform()
    except Exception:
        break

# %%
print(f'Всего получено: {len(url_list)} ссылок на товары')
print(url_list[:15])

# %%
# Переход на страницу найденного товара и парсинг

driver2 = webdriver.Chrome(options=options)
wait2 = WebDriverWait(driver2, 10)
acb_list = []

# Просмотр ссылок на телевизоры
for url in url_list:
    items_dict = {}

    driver2.get(url)
    # Заносим название
    items_dict['name'] = wait2.until(EC.presence_of_element_located((By.XPATH, "//h1"))).text
    # Заносим цену
    price = wait2.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'price-block__wallet-price')))
    try:
        items_dict['price'] = float(re.sub(r'[^\d.]+', '', price[1].text))
    except Exception:
        items_dict['price'] = None
    # Заносим бренд
    items_dict['brend'] = wait2.until(
        EC.presence_of_element_located((By.CLASS_NAME, "product-page__header-brand"))).text
    # Заносим url ссылку
    items_dict['url'] = url

    # Обрабатываем табличные данные
    table_label = wait2.until(EC.presence_of_all_elements_located((By.XPATH, '//th')))
    table_param = wait2.until(EC.presence_of_all_elements_located((By.XPATH, '//td')))
    # Заносим данные в зависимости от названия
    for i in range(len(table_label)):
        if table_label[i].text == 'Страна производства':
            items_dict['country'] = table_param[i].text
        elif table_label[i].text == 'Емкость аккумулятора (Ач)':
            try:
                val = table_param[i].text.strip()
                val, *_ = val.split()
                items_dict['capacity'] = float(re.sub(r'[^\d.]+', '', val))
            except Exception:
                items_dict['capacity'] = None
        elif table_label[i].text == 'Напряжение':
            try:
                val = table_param[i].text.strip()
                val, *_ = val.split()
                items_dict['voltage'] = float(re.sub(r'[^\d.]+', '', val))
            except Exception:
                items_dict['voltage'] = None

    # Добавляем словарь в список аккумуляторов
    acb_list.append(items_dict)

# %%
# Просмотр полученных данных

df = pd.DataFrame(items_dict)
df.head()
