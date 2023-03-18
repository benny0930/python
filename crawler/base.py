import telegram
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from inputimeout import inputimeout, TimeoutOccurred
import time
import requests
import os
import chromedriver_autoinstaller as chromedriver

bot = telegram.Bot(token='5652787798:AAHiBgILVoZG-pL55Me7XBJwODWPm7ho1BM')
isTest = False
isShowChrome = "Y"
chat_id_test = "-1001911277875"
chat_id_image = "-1001771451912" # 正式


def set(_isTest = False, _isChrome = "Y" ):
    global isTest, isShowChrome, chat_id_image
    isTest = _isTest
    isShowChrome = _isChrome
    if _isTest :
        chat_id_image = chat_id_test  # 測試用


def defaultChrome():
    chromedriver.install(cwd=True)
    chrome_options = Options()
    if isShowChrome != 'Y':
        chrome_options.add_argument('--headless')  # 啟動Headless 無頭
    chrome_options.add_argument(
        f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')
    chrome_options.add_argument('enable-logging')
    prefs = {'profile.managed_default_content_settings.images': 2}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--disable-gpu')  # 關閉GPU 避免某些系統或是網頁出錯
    driver = webdriver.Chrome(options=chrome_options)  # 套用設定
    chrome_version = driver.capabilities['browserVersion'].split(".")[0]
    driver.quit()
    print('chrome_version : ' + chrome_version)
    if (os.path.exists('./' + chrome_version )):
        service = Service('./' + chrome_version + '/chromedriver')
    else:
        service = Service('./chromedriver')
    # driver.set_page_load_timeout(30)
    driver = webdriver.Chrome(service=service, options=chrome_options)  # 套用設定
    driver.minimize_window()
    return driver


def reciprocal(sec):
    for x in range(sec):
        base_int = 10
        # print("倒數:"+str((sec-x)*base_int)+"秒")
        try:
            inputimeout(prompt="倒數:"+str((sec-x)*base_int)+"秒、輸入" + ' enter 直接跳過倒數 :  ', timeout=base_int)
            return True
        except TimeoutOccurred:
            pass
    return False
       


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


def sendTG(_chat_id, _msg):
    bot.sendMessage(chat_id=_chat_id, text=_msg, parse_mode='html')
    """
    Markdown 語法範例
    *粗體文字*
    _斜體文字_
    __底線文字__
    ~刪除線文字~
    *粗體文字 _粗斜體文字 ~粗斜體刪除線文字~ __粗斜底線文字___ 粗體文字*
    [超連結文字](超連結網址)
    `等寬字體`
    ```
    多行等寬字體
    的文字區塊
    ```
    HTML 語法範例
    <b>粗體文字</b> 或 <strong>粗體文字</strong>
    <i>斜體文字</i> 或 <em>斜體文字</em>
    <u>底線文字</u>, <ins>底線文字</ins>
    <s>刪除線文字</s> 或 <strike>刪除線文字</strike> 或 <del>刪除線文字</del>
    <b>粗體文字 <i>粗斜體文字 <s>粗斜體刪除線文字</s> <u>粗斜底線文字</u></i> 粗體文字</b>
    <a href="超連結網址">超連結文字</a>
    <code>等寬字體</code>
    <pre>多行等寬字體
    的文字區塊</pre>
    """
    # url = 'https://api.telegram.org/bot5652787798:AAHiBgILVoZG-pL55Me7XBJwODWPm7ho1BM/sendMessage?chat_id=' + \
    #     chat_id + '&parse_mode=html&text=' + msg
    # api_get(url, {})

    



def send_photo(_chat_id, _file_opened, _caption = ""):
    val = _file_opened.rsplit('.', 1)[1]
    if val == 'gif':
        # Send a gif
        bot.sendDocument(chat_id=_chat_id, document=_file_opened, caption=_caption, parse_mode='html')
    else:
        # Send a Picture
        bot.sendPhoto(chat_id=_chat_id, photo=_file_opened, caption=_caption, parse_mode='html')
    # api_url = 'https://api.telegram.org/bot5652787798:AAHiBgILVoZG-pL55Me7XBJwODWPm7ho1BM/'
    # method = "sendPhoto"
    # params = {'chat_id': chat_id , 'photo': file_opened}
    # resp = requests.post(api_url + method, params)
    # return resp