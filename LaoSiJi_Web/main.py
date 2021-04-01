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

options = webdriver.ChromeOptions()
options.add_argument(
    'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
driver = webdriver.Chrome(options=options)
driver.set_window_size(1400, 900)


def text_save(filename, data):  # filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename, 'w', encoding='utf-8')
    if data is not None:
        for i in range(len(data)):
            s = str(data[i]) + '\n'
            file.write(s)
    file.close()


def get_brand_url():
    startPath = 'C://老司机网图片/'
    if not os.path.exists(startPath):
        os.mkdir(startPath)
    startUrl = "http://www.cheshangqun.com/cars/subbrandname/%2525E5%2525A5%2525A5%2525E8%2525BF%2525AA.html"
    driver.get(startUrl)
    brands = driver.find_elements_by_xpath("//ul[@class='brand_list']/li/a")
    for brand in brands:
        urlList = []
        brandPath = startPath + brand.text
        if not os.path.exists(brandPath):
            os.mkdir(brandPath)
        url = brand.get_attribute('href')
        urlList.append(url)

        txtPath = brandPath + "/brandUrl.txt"
        text_save(txtPath, urlList)
    driver.close()


def get_pictureWeb_url():
    file = 'C://老司机网图片'
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            if f == 'brandUrl.txt':
                filePath = os.path.join(root, f)
                data = open(filePath, 'r', encoding='utf-8')
                for line in data:
                    urlList = []
                    driver.get(line)
                    time.sleep(1)
                    elements = driver.find_elements_by_xpath("//div[@class='car_filter_list']/ul/li/div/div[@class='pic']/a")
                    for element in elements:
                        print(root)
                        print(element.get_attribute('href'))
                        urlList.append(element.get_attribute('href'))

                    txtPath = root + "/pictureWebUrl.txt"
                    text_save(txtPath, urlList)


def get_picture():
    file = 'C://老司机网图片'
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            if f == 'pictureWebUrl.txt':
                filePath = os.path.join(root, f)
                data = open(filePath, 'r', encoding='utf-8')
                try:
                    for line in data:
                        driver.get(line)
                        elements = driver.find_elements_by_xpath("//div[@class='tenr']/div/div/a/img")
                        for element in elements:
                            src = element.get_attribute('src')
                            name = str(element.get_attribute('alt')).split('-')[0] + " " + str(src).split("/")[-1].split('.')[0]

                            filePath = root + '/' + name + '.jpg'

                            if not os.path.exists(filePath):
                                img = requests.get(src, headers={
                                    'User-Agent': 'Mozilla/5`.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'})
                                with open(filePath, "wb") as f:
                                    f.write(img.content)
                                    print(name)
                except Exception as err:
                    print(err)
                    continue



if __name__ == '__main__':
    get_picture()