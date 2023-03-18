import random
import base
import db
import gc
import comic
import ptt
import actor
import KPythonBot

import requests
import threading


# 檢查IP-------------------------------------------------------------------
# ip = requests.get('https://api.ipify.org').text
# if ip == "61.61.91.28":
#     print('要換IP!!!!!')
#     # base.time.sleep(30)
#     exit()


t = threading.Thread(target=KPythonBot.start, args=())
t.start()  # 開始

isLoop = True
base.set()

index = 0
while isLoop:
    # isLoop = False
    print('index = ' + str(index))
    try:
        # 兩分鐘一次PTT
        ptt.start(base, db, index)

        # 一小時一次漫畫
        # 一小時一次影片
        if index % 60 == 0:
            # base.sendTG(base.chat_id_test, '開始更新')
            comic.start(base, db)
            actor.start(base, db)
        
        if base.reciprocal(6):
            index = 0
        else:
            index += 1

        if index > 59:
            index = 0

    except Exception as e:
        print(e)
        base.sendTG(base.chat_id_test, str(e))
    gc.collect()

