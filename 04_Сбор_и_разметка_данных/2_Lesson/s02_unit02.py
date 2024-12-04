import numpy as np
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint

# Запрос веб-страницы
# url = 'https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab'
url = 'https://www.boxofficemojo.com'
# headers = {'User-Agent': UserAgent().random}
headers = {'User-Agent': UserAgent().chrome}
params = {'ref_': 'bo_nb_hm_tab'}

session = requests.Session()

response = session.get(url + '/intl', params=params, headers=headers)
# Парсинг HTML-содержимого веб-страницы с помощью Beautiful Soup
soup = BeautifulSoup(response.text, 'html.parser')
# test_link = soup.find('a', {'class': 'a-link-normal'})

rows = soup.find_all('tr')

films = []

for row in rows[2:-1]:
    film = {}
    try:
        # area_info = row.find('td',{'class':'mojo-field-type-area_id'}).find('a')
        area_info = row.find('td', {'class': 'mojo-field-type-area_id'}).findChildren()[0]
        film['area'] = [area_info.getText().strip(), url + area_info.get('href')]
    except:
        print('Exception with realeses')
        film['area'] = None

    try:
        weekend_info = row.find('td', {'class': 'mojo-field-type-date_interval'}).findChildren()[0]
        film['weekend'] = [weekend_info.getText().strip(), url + weekend_info.get('href')]
    except:
        print('Exception with realeses')
        film['weekend'] = None

    try:
        film['realeses'] = int(row.find('td', {'class': 'mojo-field-type-positive_integer'}).getText().strip())
    except:
        print('Exception with realeses')
        film['realeses'] = None

    try:
        frealeses_info = row.find('td', {'class': 'mojo-field-type-release'}).findChildren()[0]
        film['frealeses'] = [frealeses_info.getText().strip(), url + frealeses_info.get('href')]
    except:
        print('Exception with realeses')
        film['frealeses'] = None

    try:
        distributor_info = row.find('td', {'class': 'mojo-field-type-studio'}).findChildren()[0]
        film['distributor'] = [distributor_info.getText().strip(), url + distributor_info.get('href')]
    except:
        print('Exception with realeses')
        film['distributor'] = None

    try:
        film['Weekend_Gross'] = row.find('td', {'class': 'mojo-field-type-money'}).getText().strip()
    except:
        print('Exception with realeses')
        film['Weekend_Gross'] = None

    films.append(film)

pprint(films)
