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

base.set(True)
ptt.set(base, db)
driver1 = base.defaultChrome()
media = ptt.getNungvlPageImage(driver1, 'https://nungvl.net/gallerys/107779.cg', [])

base.send_media_group(base.chat_id_test, media)
