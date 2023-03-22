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
import autoShotUrl

# 檢查IP-------------------------------------------------------------------
# ip = requests.get('https://api.ipify.org').text
# if ip == "61.61.91.28":
#     print('要換IP!!!!!')
#     # base.time.sleep(30)
#     exit()


autoShotUrl.start(base, db)