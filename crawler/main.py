import threading

import base
import db
import gc
import comic
import ptt
import actor
import multiprocessing as mp



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

def loop_one_time(index):
    try:

        index = int(index)
        try:
            driver = base.defaultChrome(True)
            driver.close()
            driver.quit()
        except Exception as e:
            print(e)

        # 兩分鐘一次PTT
        ptt.start(base, db, index)

        # 一小時一次漫畫
        # 一小時一次影片
        if index % 60 == 0:
            comic.start(base, db)
            actor.start(base, db)

        if base.sleep_sec > 0:
            print("BOT 等待時間:" + str(base.sleep_sec))
            base.time.sleep(base.sleep_sec)
        gc.collect()

    except Exception as e:
        print(e)
        base.sendTG(base.chat_id_test, str(e))


index = 0
while isLoop:
    # isLoop = False
    print('index = ' + str(index))
    t = threading.Thread(target=loop_one_time, args=(str(index)))
    t.start()
    t.join()
    if base.reciprocal(6):
        index = 0
    else:
        index += 1
    if index >= 600:
        index = 0
        base.url = []



