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


def text_save(filePath, data):  # filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filePath, 'w', encoding='utf-8')
    if data is not None:
        for i in range(len(data)):
            s = str(data[i]) + '\n'
            file.write(s)
    file.close()


def getCarType_url():
    start_url = "https://www.chinatruck.org/product/"
    urlList = []

    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400, 900)
    driver.get(start_url)
    time.sleep(1)
    for i in range(28):
        try:
            elements = driver.find_elements_by_xpath("//div[@class='prics-pics']/ul/li/a")
            for element in elements:
                urlList.append(element.get_attribute('href'))

            nextPage_btn = driver.find_element_by_link_text('下一页')
            nextPage_btn.click()

        except Exception as err:
            print(err)
            continue

    return urlList


def get_NameAndPicture(filePath):
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400, 900)

    totalList = []
    data = open(filePath, "r", encoding='utf-8')
    for line in data:

        currentTypeList = []
        currentUrlList = []
        driver.get(line)
        button = driver.find_element_by_xpath("//div[@class='price-img']")
        button.click()
        carTypes = driver.find_elements_by_xpath("//div[@class='brand']/a")
        carName = driver.find_element_by_xpath("//div[@class='brand']/span").text
        currentTypeList.append(carTypes[1].text)
        currentTypeList.append(carTypes[2].text)
        currentTypeList.append(carName)

        urls = driver.find_elements_by_xpath("//ul[@id='pic']/li/a")
        for url in urls:
            currentUrlList.append(url.get_attribute('href'))
        print(currentUrlList)

        dirpath = "C://卡车网照片//" + currentTypeList[0] + "//" + currentTypeList[1] + "//" + currentTypeList[2]
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        dirpath = dirpath + '//url.txt'
        text_save(dirpath, currentUrlList)

        time.sleep(1)


def download_main(folder):
    for root, dirs, files in os.walk(folder):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            if f == 'url.txt':
                filepath = os.path.join(root, f)
                download(filepath,root)


def download(filepath,root):
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400, 900)

    data = open(filepath, "r", encoding='utf-8')
    for line in data:
        n = 0
        driver.get(line)

        carName = driver.find_element_by_class_name('all-spinfo').find_element_by_tag_name('h2').text.replace('/', "").replace('.', '').replace("*", 'X')
        print(carName)

        imgs = driver.find_elements_by_xpath("//div[@class='wg']/li/img")
        for img in imgs:
            src = img.get_attribute('src')
            downloadPath = root + "//" + carName + str(n) + '.jpg'
            if not os.path.exists(downloadPath):
                img = requests.get(src, headers={
                    'User-Agent': 'Mozilla/5`.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'})
                with open(downloadPath, "wb") as f:
                    f.write(img.content)
                    n += 1
            else:
                break
                driver.close()
    driver.close()





#carType_url = getCarType_url()
#text_save(filename,carType_url)
#filePath = "C://卡车网照片//carType_url.txt"
#get_NameAndPicture(filePath)

folder = "C://卡车网照片"
download_main(folder)



