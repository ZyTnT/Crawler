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


def main(file):
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            if f == 'type_url.txt':
                filepath = os.path.join(root, f)
                print(filepath)
                download(filepath,root)


def download(filepath, root):
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400, 900)
    data = open(filepath, 'r', encoding='utf-8')
    for line in data:
        try:
            driver.get(line)
            n = 0
            name = driver.find_element_by_xpath("//div[@class='title']").text
            if name == '':
                break
            path = root + "//" + name
            if not os.path.exists(path):
                os.makedirs(path)

            srcs = driver.find_elements_by_xpath("//div[@rrc-event-param='detail']/img")
            for src in srcs:
                url = "http:" + src.get_attribute('data-src')
                downloadPath = path + "//" + str(n) + '.webp'
                if not os.path.exists(downloadPath):
                    img = requests.get(url, headers={
                        'User-Agent': 'Mozilla/5`.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'})
                    with open(downloadPath, "wb") as f:
                        f.write(img.content)
                        n += 1
                        print(n)
                else: break

        except Exception as err:
            print(err)
            continue

if __name__ == '__main__':
    file = 'C://人人车照片'
    main(file)