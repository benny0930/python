import random

from selenium.webdriver.common.by import By

import base
import db
import gc
import comic
import ptt
import actor
import requests
import threading


# 檢查IP-------------------------------------------------------------------
# ip = requests.get('https://api.ipify.org').text
# if ip == "61.61.91.28":
#     print('要換IP!!!!!')
#     # base.time.sleep(30)
#     exit()
title = "test"
url = "http://www.playno1.com/article-38985-1.html"
base.set(True)
driver1 = base.defaultChrome()
try:
    print("-----")
    print('Playno1 : ' + title + ' / ' + url)
    print("-----")
    base.sendTG(base.chat_id_image, '<pre>' + title + '</pre>' + url)
    sql = "INSERT INTO `fa_ptt` (`name`, `url`, `title`, `createtime`, `updatetime`) VALUES ('%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))" % (
    'Beauty', url, title)

    if not base.isTest :
        db.insert(sql)

    driver1.get(url)
    print(url)
    a = driver1.find_elements(By.XPATH, '//span[@class="ui-button-text"]/..')
    a[0].click()
    base.time.sleep(2)
    all_img_a = driver1.find_elements(By.XPATH, '//img[@onload="thumbImg(this)"]')
    print(len(all_img_a))
    for one_img in all_img_a:
        print(one_img.get_attribute('src'))
        try:
            one_img.get_attribute('src').index("back.gif")
            print('YYY')
        except:
            print('NNN')
        base.send_photo(base.chat_id_image, one_img.get_attribute('src'))
except Exception as e:
    print(e)
driver1.close()