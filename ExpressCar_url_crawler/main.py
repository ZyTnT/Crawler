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
from multiprocessing import Process


def text_save(filename, data):  # filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename, 'a', encoding='utf-8')
    if data is not None:
        for i in range(len(data)):
            s = str(data[i]) + '\n'
            file.write(s)
    file.close()


def get_page_source(car_type_url):
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400, 900)
    try:
        driver.get(car_type_url)
        time.sleep(1)
        for i in range(250):
            #ele = driver.find_element_by_id("main-content")
            #driver.execute_script("arguments[0].click();", ele)
            js = 'window.scrollBy(0, 1000)'
            driver.execute_script(js)
            time.sleep(0.2)

        a = driver.page_source
        driver.close()
        return a

    except TimeoutException as err:
        return False
        print(err)


def get_picturePage_url(car_type_url):
    driverSource = get_page_source(car_type_url)
    picture_url_list = []
    if driverSource is not False:
        soup = BeautifulSoup(driverSource, "html.parser")
        divs = soup.find_all(class_="waterfall-item")
        for div in divs:
            picture_url = div.find("a", recursive=False)
            url = picture_url['href']
            picture_url_list.append(url)
        return picture_url_list


if __name__ == '__main__':
    url = "http://www.chinaso.com/newssearch/image?q=%E9%80%81%E5%BF%AB%E9%80%92"
    picture_url_list = get_picturePage_url(url)
    filename = "F://快递车照片//url.txt"
    text_save(filename,picture_url_list)