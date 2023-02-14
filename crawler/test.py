import random
import base
import db
import gc
import comic
import ptt
import actor
import requests
import threading
from selenium.webdriver.common.by import By

# 檢查IP-------------------------------------------------------------------
# ip = requests.get('https://api.ipify.org').text
# if ip == "61.61.91.28":
#     print('要換IP!!!!!')
#     # base.time.sleep(30)
#     exit()

name = 'name'
new_episode = 'new_episode'
url = 'https://www.colamanhua.com/manga-rv65322/'

driver = base.defaultChrome()
driver.get(url)
base.time.sleep(5)
# base.reciprocal(1)
last_episode = driver.find_element(By.XPATH, '//dd[@class="fed-deta-content fed-col-xs7 fed-col-sm8 fed-col-md10"]/ul/li[4]/a').text
print(last_episode)



