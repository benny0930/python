import time
import db
import requests
import os
import chromedriver_autoinstaller as chromedriver
import urllib3
import telegram
import hashlib
import traceback
import sys
import re
import threading

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from inputimeout import inputimeout, TimeoutOccurred
from PIL import Image
from io import BytesIO
from telegram import InputMediaPhoto

urllib3.disable_warnings()

bot = telegram.Bot(token='5652787798:AAHiBgILVoZG-pL55Me7XBJwODWPm7ho1BM')
isTest = False
chrome_version = ''
isShowChrome = "Y"
chat_id_test = "-1001911277875"
chat_id_image = "-1001932657196"  # 正式
chat_id_money = "-1001647881084"  # 正式
sleep_sec=0
only_driver = None
# chat_id_image = chat_id_test


def set(_isTest=False, _isChrome="Y"):
    global isTest, isShowChrome, chat_id_image
    isTest = _isTest
    isShowChrome = _isChrome
    if _isTest:
        chat_id_image = chat_id_test  # 測試用
        chat_id_money = chat_id_test  # 測試用


def defaultChrome(is_check_version=False):
    global chrome_version
    chromedriver.install(cwd=True)
    chrome_options = Options()
    if isShowChrome != 'Y':
        chrome_options.add_argument('--headless')  # 啟動Headless 無頭
    chrome_options.add_argument(
        f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')
    chrome_options.add_argument('enable-logging')
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    prefs = {'profile.managed_default_content_settings.images': 2}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--disable-gpu')  # 關閉GPU 避免某些系統或是網頁出錯

    if is_check_version or chrome_version == "":
        driver = webdriver.Chrome(options=chrome_options)  # 套用設定
        chrome_version = driver.capabilities['browserVersion'].split(".")[0]
        driver.close()
        driver.quit()
        print('chrome_version : ' + chrome_version)
    if (os.path.exists('./' + chrome_version)):
        service = Service('./' + chrome_version + '/chromedriver')
    else:
        service = Service('./chromedriver')
    # driver.set_page_load_timeout(30)
    driver = webdriver.Chrome(service=service, options=chrome_options)  # 套用設定
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    driver.minimize_window()

    t = threading.Thread(target=closeDriver, args=(driver, ))
    t.start()  # 開始

    return driver


def reciprocal(sec):
    for x in range(sec):
        base_int = 10
        # print("倒數:"+str((sec-x)*base_int)+"秒")
        try:
            inputimeout(prompt="倒數:" + str((sec - x) * base_int) + "秒、輸入" + ' enter 直接跳過倒數 :  ',
                        timeout=base_int)
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


def sendTG(_chat_id, _msg, index=0):
    global sleep_sec
    try:
        bot.sendMessage(chat_id=_chat_id, text=_msg, parse_mode='html')
    except Exception as e:
        print(str(e))
        try:
            if index < 3 and "Retry in" in str(e):
                index_new = index + 1
                numbers = [int(n) for n in re.findall('\d+', str(e))]
                print("sleep " + str(numbers[0]) + " s")
                sleep_sec = numbers[0]
                time.sleep(numbers[0])
                sleep_sec = 0
                sendTG(_chat_id, _msg, index_new)
        except:
            pass

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


def send_photo(_chat_id, _file_opened, _caption="", isPhoto=False):
    val = ""
    if not isPhoto:
        val = _file_opened.rsplit('.', 1)[1]
    if val == 'gif':
        # Send a gif
        # bot.sendDocument(chat_id=_chat_id, document=_file_opened, caption=_caption, parse_mode='html')
        sendDocument(_chat_id, _file_opened, _caption)
    else:
        # Send a Picture
        sendPhoto(_chat_id, _file_opened, _caption)
        # bot.sendPhoto(chat_id=_chat_id, photo=_file_opened, caption=_caption, parse_mode='html')
    # api_url = 'https://api.telegram.org/bot5652787798:AAHiBgILVoZG-pL55Me7XBJwODWPm7ho1BM/'
    # method = "sendPhoto"
    # params = {'chat_id': chat_id , 'photo': file_opened}
    # resp = requests.post(api_url + method, params)
    # return resp


def send_media_group(_chat_id, _media=None):
    if _media is not None and len(_media) > 0:
        print(len(_media))
        images = []
        image_names = []
        for url_one in _media:
            val = url_one.rsplit('.', 1)[1]
            if val == 'gif':
                # Send a gif
                print("GIF : " + url_one)
                # images.append(InputMediaDocument(key))
                # bot.sendDocument(chat_id=_chat_id, document=url_one, caption="", parse_mode='html')
                sendDocument(_chat_id, url_one, "")
            else:
                # Send a Picture
                print("Picture : " + url_one)
                if not os.path.exists('images'):
                    os.makedirs('images')
                image_name = 'images/image_' + str(hashlib.md5(url_one.encode()).hexdigest()) + '.jpg'
                check_image_format(url_one,image_name)
                image_names.append(image_name)
                image1 = open(image_name, 'rb')
                images.append(InputMediaPhoto(image1))
                image1.close()
            if len(images)==9:
                sendMediaGroup(_chat_id, images)
                images = []
        if len(images) > 0:
            sendMediaGroup(_chat_id, images)
        for name_one in image_names:
            remove_image(name_one)
def shotUrl(_url):
    return _url
    # return "http://ouo.io/qs/K7YG4nn8?s="+_url

    "http://ouo.io/api/K7YG4nn8?s=yourdestinationlink.com"
    r = requests.get("http://ouo.io/api/K7YG4nn8?s=" + _url, verify=False)
    return r.text


def broadcast():
    str = '<b>請多點擊鏈接</b><pre>您的點擊是我們更新的動力</pre><pre>  </pre>'

    str += '<b>友站鏈接</b><pre>歡迎您的加入</pre>'
    str += '<a href="https://t.me/KPTTBeauty">正妹圖片分享</a>\n'
    # str += '<a href="https://t.me/KPTTMoney">省錢好康情報站</a>\n'
    str += '<pre>  </pre>'

    strBeauty = str + '<pre><b>文章回顧：</b></pre>'
    name = 'Beauty'
    results = db.select("SELECT title, url FROM fa_ptt WHERE `name` = '%s' ORDER BY createtime DESC LIMIT 6" % (name))
    for result in results:
        strBeauty += '<a href="' + shotUrl(result[1]) + '">' + result[0] + '</a>\n'
    sendTG(chat_id_image, strBeauty)

    # strLifeismoney = str + '<pre><b>文章回顧：</b></pre>'
    # name = 'Lifeismoney'
    # results = db.select("SELECT title, url FROM fa_ptt WHERE `name` = '%s' ORDER BY createtime DESC LIMIT 6" % (name))
    # for result in results:
    #     strLifeismoney += '<a href="' + shotUrl(result[1]) + '">' + result[0] + '</a>\n'
    # sendTG(chat_id_money, strLifeismoney)

def sendMediaGroup(_chat_id, _images, index = 0):
    global sleep_sec
    try:
        print("發送數量：" + str(len(_images)))
        bot.send_media_group(chat_id=_chat_id, media=_images)
    except Exception as e:
        print(str(e))
        try:
            if index < 3 and "Retry in" in str(e):
                index_new = index + 1
                numbers = [int(n) for n in re.findall('\d+', str(e))]
                print("sleep " + str(numbers[0]) + " s")
                sleep_sec = numbers[0]
                time.sleep(numbers[0])
                sleep_sec = 0
                sendMediaGroup(_chat_id, _images, index_new)
        except:
            pass


def sendDocument(_chat_id, _file_opened, _caption, index = 0):
    global sleep_sec
    try:
        bot.sendDocument(chat_id=_chat_id, document=_file_opened, caption=_caption, parse_mode='html')
    except Exception as e:
        print(str(e))
        try:
            if index < 3 and "Retry in" in str(e):
                index_new = index + 1
                numbers = [int(n) for n in re.findall('\d+', str(e))]
                print("sleep " + str(numbers[0]) + " s")
                sleep_sec = numbers[0]
                time.sleep(numbers[0])
                sleep_sec = 0
                sendDocument(_chat_id, _file_opened, _caption, index_new)
        except:
            pass

def sendPhoto(_chat_id, _file_opened, _caption, index = 0):
    global sleep_sec
    try:
        bot.sendPhoto(chat_id=_chat_id, photo=_file_opened, caption=_caption, parse_mode='html')
    except Exception as e:
        print(str(e))
        try:
            if index < 3 and "Retry in" in str(e):
                index_new = index + 1
                numbers = [int(n) for n in re.findall('\d+', str(e))]
                print("sleep " + str(numbers[0]) + " s")
                sleep_sec = numbers[0]
                time.sleep(numbers[0])
                sleep_sec = 0
                sendPhoto(_chat_id, _file_opened, _caption, index_new)
        except:
            pass

def check_image_format(url, name):
    response = requests.get(url)

    # 将图片转换为 JPG 格式
    img = Image.open(BytesIO(response.content))
    img = img.convert('RGB')

    # 保存图片为 JPG 格式
    img.save(name)


def remove_image(name_one):
    # print("刪除圖片 : " + name_one)
    try:
        os.remove(name_one)
    except Exception as e:
        print(e)
        time.sleep(1)
        remove_image(name_one)

def closeDriver(driver):
    try:
        object_existed = False
        time.sleep(120) # 2分鐘後檢查瀏覽器是否關閉
        print("關閉瀏覽器")
        driver.quit()
    except Exception as e:
        print(e)
