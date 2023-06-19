import threading

import base
import db
import gc
import comic
import ptt
import actor
from datetime import datetime

# 檢查IP-------------------------------------------------------------------
# ip = requests.get('https://api.ipify.org').text
# if ip == "61.61.91.28":
#     print('要換IP!!!!!')
#     # base.time.sleep(30)
#     exit()

# try:
#     t = threading.Thread(target=KPythonBot.start, args=())
#     t.start()  # 開始
# except Exception as e:
#     print(e)


isLoop = True
base.set()


def loop_one_time_5():
    try:
        try:
            driver = base.defaultChrome(True)
            driver.close()
            driver.quit()
        except Exception as e:
            print(e)

        # 兩分鐘一次PTT
        ptt.start(base, db)
        gc.collect()
    except Exception as e:
        print(e)
        base.sendTG(base.chat_id_test, str(e))


def loop_one_time_60():
    try:
        comic.start(base, db)
        actor.start(base, db)
        gc.collect()
    except Exception as e:
        print(e)
        base.sendTG(base.chat_id_test, str(e))


index = 0
while isLoop:
    # isLoop = False
    print('index = ' + str(index))

    if index % 5 == 0:
        t1 = threading.Thread(target=loop_one_time_5)
        t1.start()
        t1.join()

    if index % 60 == 0:
        t2 = threading.Thread(target=loop_one_time_60)
        t2.start()
        t2.join()

    if base.reciprocal(6):
        index = 0
    else:
        index += 1

    if index >= 600:
        index = 0
        base.url = []
