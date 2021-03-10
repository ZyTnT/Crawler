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


def get_brand_url(start_url):
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400, 900)

    try:
        filePath = 'C://皮卡网照片/BrandURL.txt'
        urlList = []
        driver.get(start_url)
        time.sleep(1)
        urls = driver.find_elements_by_xpath("//div[@class='NodeTree']/a")
        for url in urls:
            brand = str(url.text[2:])
            brand = brand.split('(')[0]
            text = url.get_attribute('href') + ',' + brand
            urlList.append(text)
        text_save(filePath,urlList)



    except Exception as err:
        print(err)


def get_type_url():
    data = open('C://皮卡网照片//BrandURL.txt', 'r', encoding='utf-8')
    for line in data:
        line = line.replace('\n', '').split(',')
        url = line[0]
        path = 'C://皮卡网照片//' + line[1]
        txtPath = path + '//url.txt'
        if not os.path.exists(path):
            os.makedirs(path)

        typeUrlList = []
        options = webdriver.ChromeOptions()
        options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1400, 900)
        driver.get(url)
        time.sleep(1)
        elements = driver.find_elements_by_xpath("//div[@class='c0624_02']/ul/li")

        for element in elements:
            type_url = element.find_element_by_xpath("./a").get_attribute('href')
            print(type_url)
            type_name = element.find_element_by_xpath("./em").text
            print(type_name)
            text = type_url + ',' + type_name
            typeUrlList.append(text)

        text_save(txtPath, typeUrlList)
        driver.close()


def download_picture():
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400, 900)
    file = "C://皮卡网照片"

    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            if f == 'url.txt':
                filepath = os.path.join(root, f)
                data = open(filepath, "r", encoding='utf-8')
                print(data)
                n = 0
                for line in data:
                    try:
                        line = line.replace('\n', '')
                        line = line.split(",")

                        rootpath = root + "//" + line[1]

                        if not os.path.exists(rootpath):
                            os.makedirs(rootpath)

                        driver.get(line[0])
                        time.sleep(1)
                        driver.find_element_by_class_name("cms08").click()
                        pics = driver.find_elements_by_xpath("//a[@target='_blank']")
                        for pic in pics:
                            downloadPath = rootpath + "//" + str(n) + ".jpg"
                            url = pic.get_attribute('href')
                            if url!= 'https://www.cnpickups.com/info/fid-12.html':
                                if not os.path.exists(downloadPath):
                                    img = requests.get(url, headers={
                                        'User-Agent': 'Mozilla/5`.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'})
                                    with open(downloadPath, "wb") as f:
                                        f.write(img.content)
                                        n += 1

                    except Exception as err:
                        print(err)



#start_url = 'https://www.cnpickups.com/30/tupian/'
#get_brand_url(start_url)

download_picture()