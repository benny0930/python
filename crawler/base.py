from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import requests
import os
isChrome = "Y"


def set(_isChrome):
    global isChrome
    isChrome = _isChrome


def defaultChrome():
    chrome_options = Options()
    if isChrome != 'Y':
        chrome_options.add_argument('--headless')  # 啟動Headless 無頭
    chrome_options.add_argument(
        f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')
    chrome_options.add_argument('--disable-gpu')  # 關閉GPU 避免某些系統或是網頁出錯
    if(os.path.exists('C:/Users/rd3/code/kevin/chromedriver.exe')):
        s = Service('C:/Users/rd3/code/kevin/chromedriver.exe')
    else:
        s = Service('../chromedriver')
    

    driver = webdriver.Chrome(service=s, options=chrome_options)  # 套用設定
    return driver


def reciprocal(sec):
    for x in range(sec):
        print("倒數:"+str((sec-x)*10)+"秒")
        time.sleep(10)


def api_get(_url, _params):
    # api-endpoint
    # URL = "http://maps.googleapis.com/maps/api/geocode/json"

    # location given here
    # location = "delhi technological university"

    # defining a params dict for the parameters to be sent to the API
    # PARAMS = {'address':location}
    # print(_url)
    # sending get request and saving the response as response object
    r = requests.get(url=_url, params=_params)
    # print(r.json())
    # extracting data in json format
    return r.json()


def sendTG(msg):
    chat_id = '-758395812'
    url = 'https://api.telegram.org/bot5652787798:AAHiBgILVoZG-pL55Me7XBJwODWPm7ho1BM/sendMessage?chat_id=' + chat_id + '&parse_mode=html&text=' + msg
    api_get(url, {})
