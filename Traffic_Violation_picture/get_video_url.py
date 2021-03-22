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
    file = open(filename, 'a', encoding='utf-8')
    if data is not None:
        for i in range(len(data)):
            s = str(data[i]) + '\n'
            file.write(s)
    file.close()


def get_video_url(start_url):
    urlList = []
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400, 900)
    try:
        driver.get(start_url)
        time.sleep(1)
        for i in range(300):
            js = 'window.scrollBy(0, 1000)'
            driver.execute_script(js)
            time.sleep(0.2)

        urls = driver.find_elements_by_xpath("//div[@class='video_small_intro']/a")
        for url in urls:
            urlList.append(url.get_attribute('href'))
        filePath = "C://交通违规图片/不礼让行人"
        if not os.path.exists(filePath):
            os.makedirs(filePath)
        filePath = filePath + "/video_web_url.txt"
        text_save(filePath, urlList)
    except Exception as err:
        print(err)


def get_video_download_url():
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400, 900)
    file = 'C://交通违规图片/不礼让行人'
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            if f == 'video_web_url.txt':
                urlList = []
                filepath = os.path.join(root, f)
                data = open(filepath, 'r', encoding='utf-8')
                for line in data:
                    if 'baijiahao' in line:
                        try:
                            driver.get(line)
                            time.sleep(1)
                            url = driver.find_element_by_xpath("//video").get_attribute('src')
                            print(url)
                            urlList.append(url)

                        except Exception as err:
                            print(err)
                            continue
                savePath = root + '//download_video_url.txt'
                text_save(savePath, urlList)

if __name__ == '__main__':
    #start_url = 'https://www.baidu.com/sf/vsearch?pd=video&tn=vsearch&lid=b7969556000019e0&ie=utf-8&wd=%E4%B8%8D%E7%A4%BC%E8%AE%A9%E8%A1%8C%E4%BA%BA&rsv_spt=7&rsv_bp=1&f=8&oq=%E4%B8%8D%E7%A4%BC%E8%AE%A9%E8%A1%8C%E4%BA%BA&rsv_pq=b7969556000019e0&rsv_t=353bildoUGuKOaJzpWd7frDyBzM%2FiFvV4GjV8qWdUrHUXqOjufTLa4IhO1U'
    #get_video_url(start_url)
    get_video_download_url()
