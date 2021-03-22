from typing import List
import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
from multiprocessing import Process


def text_save(filename, data):  # filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename, 'a', encoding='utf-8')
    if data is not None:
        for i in range(len(data)):
            s = str(data[i]) + '\n'
            file.write(s)
    file.close()


def get_page_url():
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400, 900)

    urlList = []
    for i in range(1,10):
        strat_url = 'https://www.maodou.com/article-channel/1/' + str(i)
        driver.get(strat_url)
        urls = driver.find_elements_by_xpath("//li[@class='item']/a")
        for url in urls:
            urlList.append(url.get_attribute('href'))

    filePath = "C://毛豆新车网照片/page_url.txt"
    text_save(filePath, urlList)


def get_picture_url():
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400, 900)

    data = open("C://毛豆新车网照片/page_url.txt", 'r', encoding='utf-8')
    for line in data:
        driver.get(line)
        carType = driver.find_element_by_class_name('buy-date').text.split(' · ')[2]
        path = "C://毛豆新车网照片/" + carType

        if not os.path.exists(path):
            os.makedirs(path)

        photos = driver.find_elements_by_xpath('//div[@class="content"]/p/img')
        for photo in photos:
            url = photo.get_attribute('data-original')
            t = time.time()
            t = str(int(round(t * 1000)))
            filePath = path + '/' + t + '.jpg'

            if not os.path.exists(filePath):
                img = requests.get(url, headers={
                    'User-Agent': 'Mozilla/5`.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'})
                with open(filePath, "wb") as f:
                    f.write(img.content)
                    print(t)

            else: break



if __name__ == '__main__':
    get_picture_url()

