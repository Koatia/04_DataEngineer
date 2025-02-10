# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

# Портал об искусстве
# www.artsy.net
# https://www.programmableweb.com/api/artsy-rest-api-0

# Программа читает по API, печатает на экран и сохраняет:
# - информацию о художнике (первый запрос по API)
# - список работ художника (второй запрос по API)

import requests
import json


# Чтение данных по API из artsy.net
def get_data_from_artsy_api(link):
    """Функция возвращает словарь с информацией или пустой словарь,
    если ответ сервера отличен от 200 OK."""

    # Заголовки, User-Agent из Google Chrome
    # X-Xapp-Token выдают после регистрации и выполнения специального POST-запроса
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.61 Safari/537.36',
        'X-Xapp-Token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlcyI6IiIsInN1YmplY3RfYXBwbGljYXRpb24iOiI1ZWQ5M2Q5ZjU3YzcyODAwMTMzZDlhNTkiLCJleHAiOjE1OTE5MDAxOTEsImlhdCI6MTU5MTI5NTM5MSwiYXVkIjoiNWVkOTNkOWY1N2M3MjgwMDEzM2Q5YTU5IiwiaXNzIjoiR3Jhdml0eSIsImp0aSI6IjVlZDkzZDlmNTdjNzI4MDAwZjYyOTlmZCJ9.CE_-rSgtNDHO2ME0TcjS0yaesnKAF2x_y9OLzZJhjYM',
        'Accept': 'application/vnd.artsy-v2+json'
    }

    # Запрос и ответ
    response = requests.get(link, headers=headers)

    # Данные с сервера (словарь)
    data_from_api = {}

    # Если ответ сервера 200 Ок
    if response.ok:
        # Берем словарь
        data_from_api = response.json()

    # Возвращаем словарь с данными (полный или пустой)
    return data_from_api


# Чтение информации о художнике по API из artsy.net
def get_artist_info_from_artsy_api(artist):
    """Функция возвращает словарь с информацией о художнике.
    Если такого художника нет, то функция возвращает пустой словарь."""

    # Ссылка на API художника
    link_to_api = f'https://api.artsy.net/api/artists/{artist}'

    # Возвращаем словарь с данными (полный или пустой)
    return get_data_from_artsy_api(link_to_api)


# Чтение работ художника по API из artsy.net
def get_artist_artworks_from_artsy_api(link_to_artworks):
    """Функция возвращает словарь с работами художника.
    Если такого художника нет, то функция возвращает пустой словарь."""

    # Возвращаем словарь с данными (полный или пустой)
    return get_data_from_artsy_api(link_to_artworks)


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


# Печать на экран информации о художнике и его работах
def print_artist_info_and_artworks(artist, artworks):
    """Функция печатает на экран информацию о художнике и список его работ."""

    print(f'Имя художника: {artist.get("name")}')
    print(f'Год рождения: {artist.get("birthday")}')
    if artist.get('deathday'):
        print(f'Год смерти: {artist.get("deathday")}')
    print(f'Национальность: {artist.get("nationality")}')

    if artworks:
        # У художника есть работы
        arts_list = artworks['_embedded']['artworks']
        arts_list_count = len(arts_list)
        print(f'Количество работ художника: {arts_list_count} шт.')

        for i, item in enumerate(arts_list, 1):
            print(f'{i}) Название: {item.get("title")}')
            print(f'   Год создания: {item.get("date")}')
            print(f'   Размер: {item["dimensions"]["cm"]["text"]}')
            if item.get("collecting_institution"):
                print(f'   Владелец: {item.get("collecting_institution")}')
            if i == 5 and arts_list_count > i:
                print('.. и другие ...')
                break


if __name__ == '__main__':

    # edouard-manet, andy-warhol, edvard-munch, claude-monet
    artist_name = 'edouard-manet'

    # Получение информации по API
    artist_info = get_artist_info_from_artsy_api(artist_name)

    if artist_info:

        # Получение списка работ автора (второй запрос по API)
        artworks_link = artist_info['_links']['artworks']['href']
        artist_artworks = get_artist_artworks_from_artsy_api(artworks_link)

        # Печать на экран
        print_artist_info_and_artworks(artist_info, artist_artworks)

        # Запись в файл информации о художнике
        json_filename = f'{artist_name}-about.json'
        if save_data_to_json_file(artist_info, json_filename):
            print(f'Полная информация о художнике записана в файл {json_filename}')
        else:
            print(f'Внимание! Не удалось записать в файл {json_filename} полную информацию о художнике!')

        # Запись в файл списка работ
        json_filename = f'{artist_name}-artworks.json'
        if save_data_to_json_file(artist_artworks, json_filename):
            print(f'Полный список работ записан в файл {json_filename}')
        else:
            print(f'Внимание! Не удалось записать в файл {json_filename} полный список работ!')
