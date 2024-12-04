# Сценарий Foursquare.
#
# Напишите сценарий на языке Python, который предложит пользователю ввести интересующую его категорию (например, кофейни, музеи, парки и т.д.).
# Используйте API Foursquare для поиска заведений в указанной категории.
# Получите название заведения, его адрес и рейтинг для каждого из них.
# Скрипт должен вывести название и адрес и рейтинг каждого заведения в консоль.

# https://docs.foursquare.com/developer/reference/place-search

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
API_KEY = os.getenv("API_KEY")


import requests


def search_places():
    # Запросить у пользователя интересующую категорию и местоположение
    category = input(
        "Введите интересующую категорию (например, кофейни, музеи, парки): "
    )
    location = input(
        "Введите ваш город или местоположение (например, Москва, Нью-Йорк): "
    )

    # Задайте параметры API
    # API_KEY = "____"
    BASE_URL = "https://api.foursquare.com/v3/places/search"
    HEADERS = {"Accept": "application/json", "Authorization": API_KEY}

    # Параметры запроса
    params = {
        "query": category,  # Искомая категория
        "near": location,  # Местоположение
        "limit": 10,  # Количество результатов (например, 10)
    }

    try:
        # Отправить запрос к API Foursquare
        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        response.raise_for_status()  # Проверка на ошибки

        # Обработка ответа
        data = response.json()
        results = data.get("results", [])

        if not results:
            print(
                f"Не найдено заведений для категории '{category}' в локации '{location}'."
            )
            return

        # Выводим название, адрес и рейтинг для каждого заведения
        print(f"Найдено заведений ({len(results)}):\n")
        for place in results:
            name = place.get("name", "Нет названия")
            address = place.get("location", {}).get("formatted_address", "Нет адреса")
            rating = place.get("rating", "Рейтинг отсутствует")

            print(f"Название: {name}\nАдрес: {address}\nРейтинг: {rating}\n{'-' * 30}")

    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при запросе API: {e}")


# Запуск функции
if __name__ == "__main__":
    search_places()
