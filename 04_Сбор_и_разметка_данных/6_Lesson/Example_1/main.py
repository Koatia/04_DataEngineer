import requests
url="https://academy-public.coinmarketcap.com/optimized-uploads/c1625047385f472d81e73b207c6d3f44.png"

response = requests.get(url)
with open("image.png", "wb") as file:
    file.write(response.content)

import wget
wget.download(url)