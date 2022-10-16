from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import requests
isChrome = "N"


def set(_isChrome):
    global isChrome
    isChrome = _isChrome


def defaultChrome():
    chrome_options = Options()
    chrome_options.add_argument(
        f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')
    chrome_options.add_argument('--disable-gpu')  # 關閉GPU 避免某些系統或是網頁出錯
    s = Service('../chromedriver')

    driver = webdriver.Chrome(service=s, options=chrome_options)  # 套用設定
    return driver


def reciprocal(sec):
    for x in range(sec):
        print("倒數:"+str((sec-x)*10)+"秒")
        time.sleep(10)



