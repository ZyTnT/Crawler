import requests
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


def getPictureUrl():
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    global driver
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400, 900)

    file = 'F://老人图片'
    for root, dirs, files in os.walk(file):
        for f in files:
            try:
                if f == '不同角度url.txt':
                    filePath = os.path.join(root, f)
                    data = open(filePath, 'r', encoding='utf-8')
                    for line in data:
                        driver.get(line)
                        time.sleep(1)

                        folderName = driver.find_element_by_xpath("//img[@class='lazy']").get_attribute('title')
                        folderPath = file + '//' + folderName

                        # if not os.path.exists(folderPath):
                        #    os.makedirs(folderPath)

                        urlList = []

                        def getUrl(urlList:list):
                            pictures = driver.find_elements_by_xpath("//li[@class='list']/a")
                            for picture in pictures:
                                urlList.append(picture.get_attribute('href'))

                        while len(driver.find_elements_by_xpath("//div[@class='page']/a[@class='downPage']")) != 0:
                            if driver.find_element_by_xpath("//div[@id='login-box_home']").get_attribute('style') == "display: block;":
                                driver.find_element_by_xpath("//div[@class='login-box_close']").click()

                            getUrl(urlList)
                            time.sleep(1)
                            driver.find_element_by_xpath("//div[@class='page']/a[@class='downPage']").click()

                        getUrl(urlList)
                        txtPath = folderPath + '/' + "pictureUrl.txt"
                        text_save(txtPath, urlList)




            except Exception as err:
                print(err)
                continue


def downloadPicture():
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    global driver
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400, 900)

    file = 'F://老人图片'
    for root, dirs, files in os.walk(file):
        for f in files:
            try:
                if f == 'pictureUrl.txt':
                    filePath = os.path.join(root, f)
                    data = open(filePath, 'r', encoding='utf-8')
                    for line in data:
                        driver.get(line)
                        time.sleep(1)
                        src:str = driver.find_element_by_xpath("//a[@class='photo-img-link']").get_attribute('href')
                        name = src.split('/')[-1].replace('.jpg_', '_')
                        picturePath = root + '/' + name
                        if not os.path.exists(picturePath):
                            img = requests.get(src, headers={
                                'User-Agent': 'Mozilla/5`.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'})
                            with open(picturePath, "wb") as f:
                                f.write(img.content)
                                print(name)



            except Exception as err:
                print(err)
                continue



if __name__ == '__main__':
    downloadPicture()