import requests
from bs4 import BeautifulSoup
import os


def crawler(url):
    res = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'})
    res.encoding = res.apparent_encoding
    data = res.text
    soup = BeautifulSoup(data, "html.parser")
    ul = soup.find(class_ = 'logo-list')
    logos = ul.find_all('img')
    for logo in logos:
        src = "https://www.carlogos.org/" + logo.get('src')
        alt = logo.get('alt')[:-5]
        path = 'F://车标//' + alt+'.png'
        if not os.path.exists(path):
            img = requests.get(src, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'})
            with open(path, "wb") as f:
                f.write(img.content)



for i in range(1,9):
    url = 'https://www.carlogos.org/car-brands/list_1_' + str(i) + '.html'
    crawler(url)
