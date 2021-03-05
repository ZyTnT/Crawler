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


def is_element_present(url):
    res = requests.get(url, stream=True, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'})
    res.encoding = res.apparent_encoding
    data = res.text
    soup = BeautifulSoup(data, "html.parser")
    element = soup.find_all(attrs={'data-id': '-13'})
    if len(element) == 0:
        return False
    else:
        return True


def get_page_source(car_type_url):
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400, 900)
    try:
        driver.get(car_type_url)
        time.sleep(1)
        for i in range(200):
            ele = driver.find_element_by_class_name("cm-content-page")
            driver.execute_script("arguments[0].click();", ele)
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
        divs = soup.find_all(class_="cm-content-moudle")
        for div in divs:
            picture_url = div.find("a", recursive=False)
            url = "https://dianping.yiche.com" + picture_url['href']
            picture_url_list.append(url)
        return picture_url_list


def get_picture(car_type_url, txtpath):
    print(car_type_url)
    if is_element_present(car_type_url):
        picture_url_list = []
        picture_url_list = get_picturePage_url(car_type_url)
        if len(picture_url_list) != 0:
            url_list = []
            for picture_url in picture_url_list:
                try:
                    res = requests.get(picture_url, stream=True, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'})
                    res.encoding = res.apparent_encoding
                    data = res.text
                    soup = BeautifulSoup(data, "html.parser")
                    cartype = soup.find(class_="c-info-title")
                    if cartype is not None:
                        cartype = cartype.text
                    divs = soup.find_all(class_="details-images-block")
                    for div in divs:
                        photo = div.find('img')
                        src = str(photo.get('data-src')) + str(", ") + str(cartype)
                        url_list.append(src)
                except:
                    continue

        if not os.path.exists(txtpath):
            os.makedirs(txtpath)
        txtpath = txtpath + "url.txt"
        # path = path + str(alt) + '.png'
        # print(alt)
        if len(url_list) != 0:
            text_save(txtpath, url_list)


def process(data):
    data_copy = data.copy()
    for i in range(len(data)):
        try:
            url = data[i][2]
            path = "F://易车评论照片//" + str(data[i][0]) + "//" + str(data[i][1]) + "//"
            get_picture(url, path)
            del data_copy[i]

        except:
            continue


if __name__ == '__main__':
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    data5 = []
    data6 = []
    with open("F://易车评论照片//carlist.txt", "r", encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            line = line.split(",")
            data1.append(line)


    with open("F://易车评论照片//carlist_2.txt", "r", encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            line = line.split(",")
            data2.append(line)

    with open("F://易车评论照片//carlist_3.txt", "r", encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            line = line.split(",")
            data3.append(line)

    with open("F://易车评论照片//carlist_4.txt", "r", encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            line = line.split(",")
            data4.append(line)
    with open("F://易车评论照片//carlist_5.txt", "r", encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            line = line.split(",")
            data5.append(line)
    with open("F://易车评论照片//carlist_6.txt", "r", encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            line = line.split(",")
            data6.append(line)

    p1 = Process(target=process, args=(data1,))
    p2 = Process(target=process, args=(data2,))
    p3 = Process(target=process, args=(data3,))
    p4 = Process(target=process, args=(data4,))
    p5 = Process(target=process, args=(data5,))
    p6 = Process(target=process, args=(data6,))


    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
