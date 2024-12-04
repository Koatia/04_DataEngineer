# ПРОГРАММА ПАРСИТ hh.ru
# Сохраняет вакансии в json-файл
# Файл используется для решения домашних задач

from bs4 import BeautifulSoup
import requests
import json
import re


def get_html_page_text_from_hh(vacancy_name='Data analyst', direct_link=None):
    """Функция возвращает текст html-страницы с hh.ru по указанной вакансии.
    По умолчанию - первую страницу поиска.
    Также можно задать точную ссылку на следующую страницу.
    Если с сервера вернулась ошибка, то функция возвращает None."""

    # Базовая ссылка
    main_link = 'https://hh.ru'

    params = {
        'clusters': 'true',
        'enable_snippets': 'true',
        'salary': '',
        'st': 'searchVacancy',
        'text': vacancy_name,
        'fromSearch': 'true'
    }

    # Заголовки Google Chrome
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.61 Safari/537.36',
        'Accept': '*/*'
    }

    # Запрос и ответ
    if direct_link:
        # прямая ссылка на страницу
        link = main_link + direct_link
        response = requests.get(link, headers=headers)
    else:
        # базовая ссылка
        link = main_link + '/search/vacancy'
        response = requests.get(link, params=params, headers=headers)

    # Если ответ сервера 200 Ок, то берем данные
    if response.ok:
        return response.text
    else:
        return None


def get_salary_from_text(salary_string):
    """Функция парсит строку и возвращает три значения:
    - минимальную границу зарплаты (int),
    - максимальную границу зарплаты (int),
    - наименование валюты."""

    # Варианты:
    # до 140 000 руб.</span>
    # от 80 000 руб.</span>
    # 520-845 бел. руб.</span>
    # 120 000-150 000 руб.</span>
    # 250 000-500 000 KZT</span>

    prepared_string = salary_string.replace('\xa0', '')
    prepared_string = prepared_string.replace(' ', '')

    if prepared_string.startswith('до'):
        # Парсим вариант "до ..."
        result = re.findall(r'(\d+)(\w+\.?\w*\.?)', prepared_string)
        salary_from = None
        try:
            salary_currency = result[0][1]
        except:
            salary_currency = None
        try:
            salary_to = int(result[0][0])
        except:
            salary_to = None
        return salary_from, salary_to, salary_currency

    elif prepared_string.startswith('от'):
        # Парсим вариант "от ..."
        result = re.findall(r'(\d+)(\w+\.?\w*\.?)', prepared_string)
        salary_to = None
        try:
            salary_currency = result[0][1]
        except:
            salary_currency = None
        try:
            salary_from = int(result[0][0])
        except:
            salary_from = None
        return salary_from, salary_to, salary_currency

    else:
        # Парсим вариант, когда указаны обе границы зарплаты
        result = re.findall(r'(\d+)-(\d+)(\w+\.?\w*\.?)', prepared_string)
        try:
            salary_currency = result[0][2]
        except:
            salary_currency = None
        try:
            salary_from = int(result[0][0])
        except:
            salary_from = None
        try:
            salary_to = int(result[0][1])
        except:
            salary_to = None
        return salary_from, salary_to, salary_currency


# ПРОГРАММА

# Задаем вакансию для поиска
# Data scientist, Data analyst
searching_vacancy = 'Data scientist'

# Список для сбора всех вакансий
vacancies_data = []

# Ссылка на следующую страницу
next_page_link = None

# Бесконечный цикл прервется, когда будут просмотрены все страницы
while True:

    # Загружаем страницу с hh.ru
    page_text = get_html_page_text_from_hh(searching_vacancy, next_page_link)

    # Если есть положительный ответ от сервера с контентом
    if page_text:

        # Создаем суп и передаем текст страницы
        soup = BeautifulSoup(page_text, 'lxml')

        # Ищем div-ы с вакансиями
        all_vacancies_divs = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})

        # Цикл по всем вакансиям
        for vacancy_div in all_vacancies_divs:

            # Информация о текущей вакансии
            vacancy = {}

            # Тэг <a> с названием вакансии и ссылкой
            tag = vacancy_div.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
            vacancy_title = tag.text
            vacancy_link = tag['href']

            # ID вакансии вырезаем из ссылки
            # https://hh.ru/vacancy/37054908?query=Data%20scientist
            vacancy_id = re.search(r'/(\d+)\??', vacancy_link)
            if vacancy_id:
                try:
                    vacancy_id = int(vacancy_id.group(1))
                except ValueError:
                    vacancy_id = None

            # Тэг <a> с работодателем
            tag = vacancy_div.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})
            employer_name = tag.text.strip()

            # Тэг <span> с адресом (здесь в span-е встречаются разные варианта контента)
            tag = vacancy_div.find('span', {'data-qa': 'vacancy-serp__vacancy-address'})
            employer_city = tag.contents[0]
            employer_city = employer_city.split(',')[0]

            # Тэг <span> с зарплатой
            tag = vacancy_div.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            if tag:
                # Зарплата указана
                salary_info = get_salary_from_text(tag.text)
            else:
                # Зарплата не указана
                salary_info = (None, None, None)

            # Запись собранных данных
            vacancy['source'] = 'hh.ru'
            vacancy['id'] = vacancy_id
            vacancy['title'] = vacancy_title
            vacancy['link'] = vacancy_link
            vacancy['employer'] = employer_name
            vacancy['city'] = employer_city
            vacancy['salary_min'] = salary_info[0]
            vacancy['salary_max'] = salary_info[1]
            vacancy['salary_currency'] = salary_info[2]

            # Добавление вакансии в список
            vacancies_data.append(vacancy)

        # Ищем кнопку "дальше" для загрузки следующей страницы
        more_button_tag = soup.find('a', {'data-qa': 'pager-next'})
        if more_button_tag:
            # Есть кнопка "дальше"
            next_page_link = more_button_tag['href']
        else:
            # Просмотрели все страницы, выходим из бесконечного цикла
            break

# Запись всех собранных вакансий в файл
output_filename = searching_vacancy.lower().replace(' ', '_') + '_vacancies.json'
with open(output_filename, 'w', encoding='utf-8') as my_file:
    json.dump(vacancies_data, my_file, ensure_ascii=False, indent=4)

# Печать результатов
print(f'В файл {output_filename} сохранено {len(vacancies_data)} вакансий.')
