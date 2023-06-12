import os
import traceback
import chromedriver_autoinstaller as chromedriver
import clipboard
import urllib3
import telegram
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, DesiredCapabilities, ActionChains
import base
import random
import db
import gc
import requests
import threading
urllib3.disable_warnings()

def defaultChrome(debuggerAddress=""):
    global chrome_version
    chromedriver.install(cwd=True)
    chrome_options = Options()
    chrome_options.add_argument(
        f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')
    chrome_options.add_argument('--disable-gpu')  # 關閉GPU 避免某些系統或是網頁出錯
    # 將要封鎖的權限加入選項中
    chrome_options.add_argument("--disable-notifications")  # 封鎖通知
    chrome_options.add_argument("--disable-popup-blocking")  # 封鎖彈出窗口


    if (os.path.exists('./' + chrome_version)):
        service = Service('./' + chrome_version + '/chromedriver')
    else:
        service = Service('./chromedriver')

    if (debuggerAddress != ""):
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:" + debuggerAddress)


    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    # driver.minimize_window()
    if (debuggerAddress == ""):
        driver.maximize_window()
    return driver

def deTest(debuggerAddress=""):
    media = []
    try:
        url = "https://www.ptt.cc/bbs/Beauty/M.1685857268.A.F0E.html"
        driver.get(url)
        driver.add_cookie({'name': 'over18', 'value': '1'})
        driver.get(url)
        all_one_a = driver.find_elements(By.XPATH, '//div[@id="main-content"]/a')
        for one_a in all_one_a:
            print(one_a.get_attribute('href'))
            media.append(one_a.get_attribute('href'))
        base.send_media_group(base.chat_id_image, media)
    except Exception as e:
        print(e)


try:
    chrome_version = "113"
    debuggerAddress = ""
    debuggerAddress = "59462"
    driver = defaultChrome(debuggerAddress)
    if debuggerAddress != "":
        deTest(debuggerAddress)
except Exception as e:
    traceback.print_exc()



