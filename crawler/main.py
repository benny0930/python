import random
import base
import db
import gc
import comic
import ptt
import actor
import requests
import threading


# 檢查IP-------------------------------------------------------------------
ip = requests.get('https://api.ipify.org').text
if ip == "61.61.91.28":
    print('要換IP!!!!!')
    # base.time.sleep(30)
    exit()

isChrome = "Y"
isLoop = True
base.set(isChrome)

index = 0
while isLoop:
    # isLoop = False
    print('index = ' + str(index))
    try:
        # 兩分鐘一次PTT
        if index % 2 == 0:
            ptt.start(base, db)
        # 一小時一次漫畫
        # 一小時一次影片
        if index % 60 == 0:
            base.sendTG('-758395812', '開始更新')
            comic.start(base, db)
            actor.start(base, db)
        
        if base.reciprocal(6):
            index = 0
        else:
            index += 1
        if index > 60:
            index = 0

    except Exception as e:
        print(e)
        base.sendTG('-758395812', str(e))
    gc.collect()

