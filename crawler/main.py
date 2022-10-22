import random
import base
import db
import gc
import comic
import actor
import requests


# 檢查IP-------------------------------------------------------------------
ip = requests.get('https://api.ipify.org').text
if ip == "61.61.91.28" :
    print('要換IP!!!!!')
    base.time.sleep(30)
    exit()

# 更新演員及作品-------------------------------------------------------------------

isChrome = "N"
isLoop = True
base.set(isChrome)
while isLoop:
    isLoop = False
    base.sendTG('開始更新')
    try:
        comic.start(base, db)
        # base.reciprocal(2)
        actor.start(base, db)
    except Exception as e:
        print(e)
        base.sendTG(str(e))
    # base.reciprocal(60*6+random.randrange(1, 6))
    gc.collect()

