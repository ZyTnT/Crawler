import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time


def get_full_page(url):
    global driver
    driver = webdriver.Chrome()
    driver.set_window_size(1400, 900)
    try:
        driver.get(url)
        time.sleep(1)
        #ActionChains(driver).move_by_offset(0, 0).click().perform();

        for i in range(10):

            driver.find_element_by_tag_name('body').send_keys(Keys.SPACE)
            time.sleep(0.2)

        a = driver.page_source
        driver.close()
        return a

    except TimeoutException as err:
        print(err)


def crawler(url):
    #res = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'})
    #res.encoding = res.apparent_encoding
    #data = res.text
    soup = BeautifulSoup(get_full_page(url), "html.parser")
    div = soup.find(class_ = 'uibox-con')
    #div = soup.find(attrs={'id' : 'imgList'})
    n = 0
    photos = div.find_all('img')
    for photo in photos:
        src = 'https:' + photo.get('src')
        #alt = photo.get('alt')
        alt = n
        path = 'F://汽车照片//御捷//御捷E驰//'

        if not os.path.exists(path):
            os.makedirs(path)

        #path = path + 'other' + str(alt) + '.jpg'
        path = path + str(alt) + '.jpg'
        print(alt)
        if not os.path.exists(path):
            img = requests.get(src, headers={'User-Agent':'Mozilla/5`.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'})
            with open(path, "wb") as f:
                f.write(img.content)
            n += 1



url = 'https://car.autohome.com.cn/pic/series-t/4508-1.html#pvareaid=2042222#pvareaid=2042222'
crawler(url)