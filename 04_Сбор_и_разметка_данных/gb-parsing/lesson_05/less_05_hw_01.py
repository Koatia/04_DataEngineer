# 1) Написать программу, которая собирает входящие письма из своего
# или тестового почтового ящика и сложить данные о письмах в базу данных
# * от кого,
# * дата отправки,
# * тема письма,
# * текст письма полный

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from datetime import datetime as dt
from datetime import timedelta
from pymongo import MongoClient
import time
import re

# Логин и пароль от почты!!!!!!!!!!!!!!!!
MAILBOX_LOGIN = '-----------------------'
MAILBOX_PASSWORD = '--------------------'
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def get_date_from_string(date_string):
    """
    Функция парсит строку, достает из нее и возвращает дату.
    Варианты строк на входе:
    Сегодня, 13:22
    Вчера, 20:08
    11 июня, 15:18
    24 декабря 2019, 11:45
    """
    # Словарь с месяцами
    months = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12
    }

    # Проверяем формат даты на входе
    if date_string.startswith('Сегодня'):
        # На входе формат: "Сегодня, 13:22"
        sr = re.search(r'\w+, (\d+):(\d+)', date_string)
        try:
            date = dt.now()
            date = dt(day=date.day, month=date.month, year=date.year,
                      hour=int(sr.group(1)), minute=int(sr.group(2)))
        except:
            date = None
    elif date_string.startswith('Вчера'):
        # На входе формат: "Вчера, 20:08"
        sr = re.search(r'\w+, (\d+):(\d+)', date_string)
        try:
            date = dt.now() - timedelta(days=1)
            date = dt(day=date.day, month=date.month, year=date.year,
                      hour=int(sr.group(1)), minute=int(sr.group(2)))
        except:
            date = None
    else:
        # На входе возможны два варианта даты:
        # 11 июня, 15:18
        # 24 декабря 2019, 11:45
        # Проверка наличия года в строке, чтобы определиться с форматом входной строки
        year_search = re.search(r'\d{4}', date_string)
        if year_search:
            # Нашли в строке год (прошлогодние и старые письма)
            sr = re.search(r'(\d+) (\w+) (\d{4}), (\d+):(\d+)', date_string)
            try:
                date = dt(day=int(sr.group(1)), month=months[sr.group(2)], year=int(sr.group(3)),
                          hour=int(sr.group(4)), minute=int(sr.group(5)))
            except:
                date = None
        else:
            # Нет года в строке (письма текущего года)
            sr = re.search(r'(\d+) (\w+), (\d+):(\d+)', date_string)
            try:
                date = dt(day=int(sr.group(1)), month=months[sr.group(2)], year=dt.now().year,
                          hour=int(sr.group(3)), minute=int(sr.group(4)))
            except:
                date = None
    return date


def get_letter_item(date, sender, subj, body):
    """Функция возвращает словарь с одним письмом."""
    return {
        'date': date,
        'sender': sender,
        'subject': subj,
        'body': body
    }


# Список для сбора писем
all_letters = list()

# Настройка параметров браузера (на весь экран)
chrome_options = Options()
chrome_options.add_argument('start-maximized')

# Создаем драйвер с параметрами браузера
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)

# Загружаем страницу
driver.get('https://mail.ru/')

# Проверка страницы
assert "Mail.ru" in driver.title

# Вводим логин. Сабмитим.
login_input = driver.find_element_by_id('mailbox:login')
login_input.send_keys(MAILBOX_LOGIN)
login_input.submit()

# Ждем, когда появится поле с паролем. Вводим пароль. Сабмитим
password_input = driver.find_element_by_id('mailbox:password')
password_input.send_keys(MAILBOX_PASSWORD)
password_input.submit()

# Ждем, когда страница переключится на папку "Входящие"
WebDriverWait(driver, 10).until(
    ec.title_contains('Входящие')
)

# Проверка страницы
assert "Входящие" in driver.title

# Находим и кликаем на самое первое письмо в списке
letter = driver.find_element_by_class_name('js-letter-list-item')
letter.click()

# Ждем, когда перегрузится страница с письмом
WebDriverWait(driver, 10).until(
    ec.title_contains('Почта')
)

# Проверка страницы
assert "Почта" in driver.title

# Находим кнопку "Следующее", через которую будем в цикле
# переключаться на следующее письмо, пока кнопка доступна
next_letter_tag = driver.find_element_by_xpath('//span[@title="Следующее"]')

# В цикле проходим по всем письмам.
# Внутри письма собираем всю необходимую информацию и переходим на следующее письмо
while True:

    # Ждем, чтобы не забанили и страница подгрузилась
    time.sleep(1)

    # Отправитель
    sender_tag = driver.find_element_by_xpath('//div[@class="letter__author"]//span[@class="letter-contact"]')
    letter_sender = f'{sender_tag.text} <{sender_tag.get_attribute("title")}>'

    # Дата письма
    date_tag = driver.find_element_by_xpath('//div[@class="letter__date"]')
    letter_date = get_date_from_string(date_tag.text)

    # Полный текст письма
    body_tag = driver.find_element_by_xpath('//div[contains(@id, "_BODY")]')
    letter_body = body_tag.text

    # Тема письма
    subject_tag = driver.find_element_by_xpath('//h2[@class="thread__subject thread__subject_pony-mode"]')
    letter_subject = subject_tag.text

    # Добавляем письмо в список
    all_letters.append(get_letter_item(letter_date, letter_sender, letter_subject, letter_body))

    # Переходим к следующему письму, если элемент доступен (нет атрибута disabled).
    # Выходим из цикла, если у элемента появился атрибут disabled (последнее письмо).
    if next_letter_tag.get_attribute('disabled') is None:
        next_letter_tag.click()
    else:
        break

# Закрываем Selenium
driver.quit()

# ЗАПИСЬ ВСЕХ СОБРАННЫХ ВАКАНСИЙ В БАЗУ ДАННЫХ

# Подключение к базе данных MongoDB
client = MongoClient('localhost', 27017)
db = client['gb_mailbox']
db_inbox = db.inbox

# Очищаем коллекцию. Удаляем все элементы
db_inbox.delete_many({})

# Запись сразу всех писем (список словарей)
result = db_inbox.insert_many(all_letters)

# Печать результата
print(f'Скрапинг почтового ящика завершен.')
print(f'В базу данных записано {len(result.inserted_ids)} писем.')
