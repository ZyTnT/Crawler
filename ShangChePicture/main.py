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
    file = 'C://商车网客车图片'
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            if f == 'bigTypeUrl.txt':
                filePath = os.path.join(root, f)
                data = open(filePath, 'r', encoding='utf-8')
                for line in data:
                    driver.get(line)
                    element = driver.find_element_by_xpath('//dl[@class="clear"]')
                    target = element.find_elements_by_xpath('.//dd/ul/li/a')
                    for url in target:
                        link = url.get_attribute('href')
                        name = url.text
                        rootPath = root + '/' + name
                        if not os.path.exists(rootPath):
                            os.makedirs(rootPath)
                        textPath = rootPath + '/brandUrl.txt'
                        f = open(textPath, 'w', encoding='utf-8')
                        f.write(link)


def get_smallBrand_url():
    file = 'C://商车网客车图片'
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
                    element = driver.find_elements_by_xpath('//dl[@class="clear"]')[1]
                    target = element.find_elements_by_xpath('.//dd/ul/li/a')
                    for url in target:
                        urlList.append(url.get_attribute('href'))
                        name = url.text
                        rootPath = root + '/' + name
                        if not os.path.exists(rootPath):
                            os.makedirs(rootPath)
                        textPath = rootPath + '/smallBrandUrl.txt'
                        text_save(textPath, urlList)


def get_length_url():
    file = 'C://商车网客车图片'
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            try:
                if f == 'smallBrandUrl.txt':
                    filePath = os.path.join(root, f)
                    data = open(filePath, 'r', encoding='utf-8')
                    for line in data:
                        driver.get(line)
                        lengths1 = driver.find_elements_by_xpath('//dl[@class="clear"]')[2]
                        lengths = lengths1.find_elements_by_xpath('.//dd/ul/li/a')
                        for length in lengths:
                            link = length.get_attribute('href')
                            name = length.text
                            rootPath = root + '/' + name
                            if not os.path.exists(rootPath):
                                os.makedirs(rootPath)
                            textPath = rootPath + '/length.txt'
                            f = open(textPath, 'w', encoding='utf-8')
                            f.write(link)
            except Exception as err:
                print(err)
                continue


def get_humanNum_url():
    file = 'C://商车网客车图片'
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            try:
                if f == 'length.txt':
                    filePath = os.path.join(root, f)
                    data = open(filePath, 'r', encoding='utf-8')
                    for line in data:
                        driver.get(line)
                        lengths1 = driver.find_elements_by_xpath('//dl[@class="clear"]')[3]
                        lengths = lengths1.find_elements_by_xpath('.//dd/ul/li/a')
                        for length in lengths:
                            link = length.get_attribute('href')
                            name = length.text
                            rootPath = root + '/' + name
                            if not os.path.exists(rootPath):
                                os.makedirs(rootPath)
                            textPath = rootPath + '/humanNum.txt'
                            f = open(textPath, 'w', encoding='utf-8')
                            f.write(link)
            except Exception as err:
                print(err)
                continue


def get_power_url():
    file = 'C://商车网客车图片'
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            try:
                if f == 'humanNum.txt':
                    filePath = os.path.join(root, f)
                    data = open(filePath, 'r', encoding='utf-8')
                    for line in data:
                        driver.get(line)
                        power1 = driver.find_elements_by_xpath('//dl[@class="clear"]')[4]
                        power = power1.find_elements_by_xpath('.//dd/ul/li/a')
                        for url in power:
                            link = url.get_attribute('href')
                            name = url.text
                            rootPath = root + '/' + name
                            if not os.path.exists(rootPath):
                                os.makedirs(rootPath)
                            textPath = rootPath + '/powerUrl.txt'
                            f = open(textPath, 'w', encoding='utf-8')
                            f.write(link)
            except Exception as err:
                print(err)
                continue


def get_pictureWeb_url():
    file = 'C://商车网客车图片/专用客车'
    for root, dirs, files in os.walk(file):
        for f in files:
            try:
                if f == 'length.txt':
                    if not os.path.exists(root + '/pictureUrl.txt'):
                        filePath = os.path.join(root, f)
                        data = open(filePath, 'r', encoding='utf-8')
                        for line in data:
                            driver.get(line)
                            #time.sleep(0.5)
                            if len(driver.find_elements_by_class_name("noPro")) == 0:
                                urlList = []
                                n = 0
                                while True:
                                    print(driver.current_url)
                                    elements = driver.find_elements_by_css_selector("[class='proItem clear']")
                                    print(len(elements))
                                    for element in elements:
                                        element = element.find_element_by_xpath('.//a')
                                        url = element.get_attribute('href') + "_3-1"
                                        urlList.append(url)
                                        print(url)
                                    if len(driver.find_elements_by_class_name("nextprev")) != 0 and n<3:
                                            driver.find_element_by_class_name("nextprev").click()
                                            n+=1
                                    else:
                                        break

                                savePath = root + '/pictureUrl.txt'
                                if len(urlList) != 0:
                                    text_save(savePath, urlList)

                            else:
                                continue

            except Exception as err:
                print(err)
                continue


def downloadPicture():
    file = 'C://商车网客车图片'
    for root, dirs, files in os.walk(file):
        for f in files:
            try:
                if f == 'pictureUrl.txt':
                    filePath = os.path.join(root, f)
                    data = open(filePath, 'r', encoding='utf-8')
                    for line in data:
                        driver.get(line)
                        elements = driver.find_elements_by_xpath("//ul[@class='mConCarImg']/li/a/img")
                        print(len(elements))
                        srcList = []
                        for element in elements:
                            srcList.append(element.get_attribute('src'))
                        for src in srcList:
                            #t = time.time()
                            #t = str(int(round(t * 1000)))
                            name = str(src).split("/")[-1][:-4]
                            print(name)
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
    downloadPicture()
