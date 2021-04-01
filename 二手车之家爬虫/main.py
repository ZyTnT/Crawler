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
    start_url = "https://www.che168.com/china/dazhong/#pvareaid=108402#listfilterstart"
    driver.get(start_url)

    driver.find_element_by_xpath("//a[@eventkey='c_pc_carlist_pinpai_more']").click()
    elements = driver.find_elements_by_xpath("//div[@id='brandshow']/div/dl/dd/a")
    for element in elements:
        urlList = []
        name = element.text
        url = element.get_attribute('href')
        urlList.append(url)

        rootPath = "C://二手车之家图片/" + name
        txtPath = rootPath + "/brandUrl.txt"
        if not os.path.exists(rootPath):
            os.makedirs(rootPath)

        text_save(txtPath, urlList)

        print(element.text)
        print(url)
    driver.close()


def get_type_url():
    file = 'C://二手车之家图片'
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            try:
                if f == 'brandUrl.txt':
                    filePath = os.path.join(root, f)
                    data = open(filePath, 'r', encoding='utf-8')
                    for line in data:
                        driver.get(line)
                        time.sleep(2)
                        if len(driver.find_elements_by_xpath("//a[@eventkey='c_pc_carlist_chexi_more']")) != 0:
                            driver.find_element_by_xpath("//a[@eventkey='c_pc_carlist_chexi_more']").click()
                            elements = driver.find_elements_by_xpath("//div[@id='seriesShow']/div/dl")
                            for element in elements:
                                carType = element.find_element_by_xpath(".//dt").text

                                series = element.find_elements_by_xpath(".//dd/a")
                                for serie in series:
                                    urlList = []
                                    urlList.append(serie.get_attribute('href'))
                                    title = serie.get_attribute('title')

                                    carTypePath = root + '/' + carType + '/' + title
                                    if not os.path.exists(carTypePath):
                                        os.makedirs(carTypePath)

                                    txtPath = carTypePath + '/typeUrl.txt'
                                    text_save(txtPath, urlList)

                        else:
                            element = driver.find_element_by_css_selector("[class='condition-list condition-series fn-clear js-screening-up']")
                            series = element.find_elements_by_xpath(".//a")
                            for serie in series:
                                urlList = [serie.get_attribute('href')]
                                title = serie.get_attribute('title')
                                print(title)

                                carTypePath = root + '/' + title
                                if not os.path.exists(carTypePath):
                                    os.makedirs(carTypePath)

                                txtPath = carTypePath + '/typeUrl.txt'
                                text_save(txtPath, urlList)

            except Exception as err:
                print(err)
                continue


def get_pictureWeb_url():
    file = 'C://二手车之家图片'
    for root, dirs, files in os.walk(file):
        for f in files:
            try:
                if f == 'typeUrl.txt':
                    filePath = os.path.join(root, f)
                    data = open(filePath, 'r', encoding='utf-8')
                    for line in data:
                        driver.get(line)
                        time.sleep(2)
                        urlList = []

                        while True:
                            elements = driver.find_elements_by_xpath("//div[@id='goodStartSolrQuotePriceCore0']/ul/li/a")
                            for element in elements:
                                urlList.append(element.get_attribute('href'))

                            nextBtn = driver.find_elements_by_xpath("//a[@class='page-item-next']")
                            if len(nextBtn) != 0:
                                driver.find_element_by_xpath("//a[@class='page-item-next']").click()
                                time.sleep(2)

                            else:break

                        txtPath = root + '/pictureWebUrl.txt'
                        print(len(urlList))
                        if len(urlList) != 0:
                            text_save(txtPath, urlList)

            except Exception as err:
                print(err)
                continue


def download_picture():
    file = 'C://二手车之家图片'
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            if f == 'pictureWebUrl.txt':
                filePath = os.path.join(root, f)
                data = open(filePath, 'r', encoding='utf-8')
                for line in data:
                    try:
                        srcList = []
                        driver.get(line)
                        time.sleep(2)
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(3)
                        elements = driver.find_elements_by_xpath("//div[@id='pic_li']/a/img")
                        for element in elements:
                            srcList.append(element.get_attribute('src'))
                            for src in srcList:
                                # t = time.time()
                                # t = str(int(round(t * 1000)))
                                name = driver.find_element_by_class_name("car-brand-name").text + " " + str(src).split("/")[-1][:-4]
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
    download_picture()