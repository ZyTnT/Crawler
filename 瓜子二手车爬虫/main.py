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
import re
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

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
    start_url = "https://www.guazi.com/www/buy/c-1/#bread"
    driver.get(start_url)
    element = driver.find_element_by_css_selector("[class='dd-all clearfix js-brand js-option-hid-info']")
    brands = element.find_elements_by_xpath(".//ul/li/p/a")
    for brand in brands:
        urlList = []
        name = brand.get_attribute('textContent')
        brandUrl = brand.get_attribute('href')
        urlList.append(brandUrl)

        rootPath = "F://瓜子二手车图片/" + name
        txtPath = rootPath + "/brandUrl.txt"
        if not os.path.exists(rootPath):
            os.makedirs(rootPath)

        text_save(txtPath, urlList)

    driver.close()


def get_type_url():
    file = 'F://瓜子二手车图片/'
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
                        if len(driver.find_elements_by_css_selector("[class='carlist clearfix js-top']")) != 0:
                            if len(driver.find_elements_by_xpath("//span[@data-local='js-tag']")) != 0:
                                driver.find_element_by_xpath("//span[@data-local='js-tag']").click()
                            elements = driver.find_element_by_css_selector("[class='dd-car js-tag js-option-hid-info']")
                            lis = elements.find_elements_by_xpath(".//ul/li")
                            for li in lis:
                                type = li.find_element_by_xpath('.//label').get_attribute('textContent')
                                urls = li.find_elements_by_xpath('.//p/a')
                                for url in urls:
                                    urlList = []
                                    carType = url.get_attribute('textContent').split('  ')[0]
                                    urlList.append(url.get_attribute('href'))
                                    folderPath = root + '/' + type + '/' + carType

                                    if not os.path.exists(folderPath):
                                        os.makedirs(folderPath)

                                    txtPath = root + '/' + type + '/' + carType + '/typeUrl.txt'

                                    text_save(txtPath,urlList)
                                    print(carType)

            except Exception as err:
                print(err)
                continue


def get_carWeb_url():
    file = 'F://瓜子二手车图片/'
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            try:
                if f == 'typeUrl.txt':
                    filePath = os.path.join(root, f)
                    data = open(filePath, 'r', encoding='utf-8')
                    for line in data:
                        driver.get(line)
                        time.sleep(1)
                        urlList = []
                        if len(driver.find_elements_by_css_selector("[class='carlist clearfix js-top']")) != 0:
                            if len(driver.find_elements_by_css_selector("[class='pageLink clearfix']")) != 0:
                                flag = True
                                while(flag == True):
                                    element = driver.find_element_by_css_selector("[class='carlist clearfix js-top']")
                                    webs = element.find_elements_by_xpath(".//li/a")
                                    for web in webs:
                                        urlList.append(web.get_attribute('href'))

                                    pageLink = driver.find_element_by_css_selector("[class='pageLink clearfix']")
                                    if len(pageLink.find_elements_by_xpath('.//li/a[@class="next"]')) == 0:
                                        flag = False
                                        txtPath = root + '/pictureUrl.txt'
                                        text_save(txtPath, urlList)

                                    else:
                                        pageLink.find_element_by_xpath('.//li/a[@class="next"]').click()
                                        time.sleep(1)

                            else:
                                element = driver.find_element_by_css_selector("[class='carlist clearfix js-top']")
                                webs = element.find_elements_by_xpath(".//li/a")
                                for web in webs:
                                    urlList.append(web.get_attribute('href'))

                                txtPath = root + '/pictureUrl.txt'
                                text_save(txtPath, urlList)


            except Exception as err:
                print(err)
                continue


def download_Picture():
    file = 'F://瓜子二手车图片/'

    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    driver = webdriver.Chrome(desired_capabilities=capa)
    wait = WebDriverWait(driver, 5)


    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            try:
                if f == 'pictureUrl.txt':
                    flag = True
                    for root2, dirs2, files2 in os.walk(root):
                        for f2 in files2:
                            if '.jpg' in f2:
                                flag = False

                    if flag == True:
                        filePath = os.path.join(root, f)
                        data = open(filePath, 'r', encoding='utf-8')
                        for line in data:
                            driver.get(line)

                            wait.until(EC.presence_of_element_located((By.XPATH, '//ul[@class="det-picside"]/li/img')) and EC.presence_of_element_located((By.CLASS_NAME,'titlebox')))

                            name = driver.find_element_by_class_name('titlebox').text.replace(" 严选车",'').replace(' 0过户','')
                            print(name)

                            folderPath = root + '/' + name
                            if not os.path.exists(folderPath):
                                os.makedirs(folderPath)

                            photoNumber = driver.find_element_by_xpath('//li[@data-gzlog="tracking_type=click&eventid=0220050000099049"]/a').get_attribute('textContent')
                            photoNumber = int(re.sub('\D','',photoNumber))

                            photos = driver.find_elements_by_xpath('//ul[@class="det-picside"]/li/img')[:(photoNumber)]
                            for photo in photos:
                                src = photo.get_attribute('data-src').split('?')[0]
                                pictureName = str(src.split('/')[-1])
                                filePath = folderPath + '/' + pictureName

                                if not os.path.exists(filePath):
                                    img = requests.get(src, headers={
                                        'User-Agent': 'Mozilla/5`.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'})
                                    with open(filePath, "wb") as f:
                                        f.write(img.content)
                                        print(src)


            except Exception as err:
                print(err)
                continue


if __name__ == '__main__':
    #get_brand_url()
    #get_type_url()
    #get_carWeb_url()
    download_Picture()