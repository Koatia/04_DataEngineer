# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json
from datetime import datetime


# Чтение данных по API из GitHub.com
def get_data_from_github_api(username):
    """Функция возвращает словарь с репозиториями указанного пользователя на GitHub.com.
    Если у пользователя нет репозиториев, то функция возвращает пустой словарь.
    Если такого пользователя нет, то функция возвращает None."""

    # Ссылка на API пользователя
    link_to_user_repos = f'https://api.github.com/users/{username}/repos'

    # Заголовки Google Chrome
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.61 Safari/537.36',
        'Accept': '*/*'
    }

    # Параметры запроса
    params = {
        'type': 'owner',
        'sort': 'created',
        'direction': 'desc'
    }

    # Запрос и ответ
    response = requests.get(link_to_user_repos, headers=headers, params=params)

    # Данные с сервера (словарь)
    data_from_api = {}

    # Если ответ сервера 200 Ок, то берем данные
    if response.ok:

        data_from_api = response.json()

        # Если пользователя нет, то возвращаем None
        if data_from_api and data_from_api[0].get('message') == 'Not Found':
            data_from_api = None

    # Возвращаем словарь с данными (полный или пустой)
    return data_from_api


# Сохранение данных в json-файл
def save_data_to_json_file(data, filename):
    """Функция сохраняет данные в json-файл.
    Вовзращает True, если все ОК.
    Возвращает False, если при записи произошел сбой."""

    # Запись файла через try-except, чтобы отловить ошибки
    try:
        with open(filename, 'w', encoding='utf-8') as my_file:
            json.dump(data, my_file, ensure_ascii=False, indent=4)
    except IOError:
        return False
    else:
        return True


# Печать на экран
def print_data(username, data):
    """Функция печатает на экран данные, полученные с GitHub.com"""

    if data is None:
        # Нет такого пользователя
        print(f'На GitHub.com не существует пользователя {username}!')

    elif data:
        # Есть репозитории у пользователя
        print(f'Имя пользователя: {username}')
        print(f'Количество репозиториев на GitHub.com: {len(data)} шт.')
        for i, repo in enumerate(data, 1):
            whitespaces = len(str(i)) * ' '
            original_format = '%Y-%m-%dT%H:%M:%SZ'  # 2020-04-08T17:59:52Z
            ru_format = '%d.%m.%Y'
            created_date = datetime.strptime(repo.get("created_at"), original_format)
            created_date = created_date.strftime(ru_format)
            print(f'{i}) Название: {repo.get("name")}')
            if repo.get("description"):
                print(f'{whitespaces}  Описание: {repo.get("description")}')
            print(f'{whitespaces}  Дата создания: {created_date}')
            print(f'{whitespaces}  Ссылка: {repo.get("html_url")}')

    else:
        # У пользователя нет репозиториев
        print(f'У пользователя {github_user} на GitHub.com нет репозиториев.')


if __name__ == '__main__':

    # Получение информации по API
    github_user = 'RomanSharavin'
    user_repositories = get_data_from_github_api(github_user)

    # Печать на экран
    print_data(github_user, user_repositories)

    # Запись в файл
    json_filename = f'repos_of_{github_user}.json'
    if save_data_to_json_file(user_repositories, json_filename):
        print(f'Полная информация записана в файл {json_filename}')
    else:
        print(f'Внимание! Не удалось записать в файл {json_filename} полную информацию!')
