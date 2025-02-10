import requests
import json

import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

api_key = os.getenv('api_key')
url = 'https://api.foursquare.com/v3/places/search'

city = input("Введите название города: ")
category = input("Введите категорию (cafe, fitness, memorial & etc): ")

params = {
    'near': city,
    'limit': 5,
    'query': category,
    'fields': 'name,location,rating'
}

headers = {
    'Accept': 'application/json',
    'Authorization': api_key
}

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    data = json.loads(response.text)
    for place in data['results']:
        print("\nНазвание:", place.get('name'))
        print("Адрес:", place.get('location').get('formatted_address'))
        print("Рейтинг:", place.get('rating', 'не определился'))
else:
    print("Запрос API завершился неудачей с кодом состояния:", response.status_code)
    print(response.text)
