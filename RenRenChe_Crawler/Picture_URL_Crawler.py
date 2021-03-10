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
    file = open(filename, 'w', encoding='utf-8')
    if data is not None:
        for i in range(len(data)):
            s = str(data[i]) + '\n'
            file.write(s)
    file.close()


def get_brand_url():
    start_url = "https://www.renrenche.com/cn/ershouche/?plog_id=692479cac871a09cd29ed5a23e3c4fca"
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400, 900)
    try:
        urlList = []
        driver.get(start_url)
        time.sleep(1)
        elements = driver.find_elements_by_class_name("bn")
        for element in elements:
            urls = element.find_elements_by_tag_name("a")
            for url in urls:
                url = "https://www.renrenche.com/" + url.get_attribute('href')
                urlList.append(url)
        text_save("C://人人车照片/Brand_URL.txt", urlList)

    except Exception as err:
        print(err)


def get_carType_url():
    brandUrl = open("C://人人车照片/Brand_URL.txt", 'r' , encoding='utf-8')
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400, 900)
    for brand in brandUrl:
        try:
            carType_url = []
            driver.get(brand)
            name = driver.find_element_by_xpath("//p[@rrc-event-name='position3']").text
            path = "C://人人车照片/" + name
            if not os.path.exists(path):
                os.makedirs(path)

            while True:
                btn = driver.find_element_by_xpath("//a[@rrc-event-name='switchright']")
                if btn.get_attribute('href') != 'javascript:void(0);':
                    page_urls = driver.find_elements_by_xpath("//li[@data-is-near='0']/a[@rrc-event-param='search']")
                    for page_url in page_urls:
                        url = "https://www.renrenche.com/" + page_url.get_attribute('href')
                        carType_url.append(url)
                    btn.click()

                else:
                    page_urls = driver.find_elements_by_xpath("//li[@data-is-near='0']/a[@rrc-event-param='search']")
                    for page_url in page_urls:
                        url = "https://www.renrenche.com/" + page_url.get_attribute('href')
                        carType_url.append(url)
                    break

            txtPath = path + '/type_url.txt'
            text_save(txtPath, carType_url)

        except Exception as err:
            print(err)


get_carType_url()
