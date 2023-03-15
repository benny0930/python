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
# ip = requests.get('https://api.ipify.org').text
# if ip == "61.61.91.28":
#     print('要換IP!!!!!')
#     # base.time.sleep(30)
#     exit()

isLoop = True
base.set()

index = 0
while isLoop:
    # isLoop = False
    print('index = ' + str(index))
    try:
        # 一小時一次影片
        if index % 30 == 0:
            ptt.set(base, db)
            ptt.Playno1()

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

