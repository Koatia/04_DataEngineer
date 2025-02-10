import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint

# Запрос веб-страницы
url = 'https://gb.ru'
headers = {'User-Agent': UserAgent().chrome}
params = {'page': 1}

session = requests.Session()

all_posts = []

while True:
    response = session.get(url + '/posts', headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all('div', {'class': 'post-item'})
    if not posts:
        break

    for post in posts:
        post_info = {}

        name_info = post.find('a', {'class': 'post-item__title'})
        post_info['name'] = name_info.getText()
        post_info['url'] = url + name_info.get('href')

        rating_info = post.find('div', {'class': 'text-muted'}).findChildren('span')
        post_info['views'] = int(rating_info[0].getText())
        post_info['comments'] = int(rating_info[1].getText())

        all_posts.append(post_info)
    print(f"Обработана {params['page']} страница")
    params['page'] += 1

pprint(all_posts)
print(len(all_posts))
