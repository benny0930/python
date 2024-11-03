# coding: utf-8
import inspect
import db
import json
import re
import os
import shutil
import instaloader
import time

from base import Base
from playwright.sync_api import sync_playwright
from datetime import datetime
from PTTLibrary import PTT
import sys
import yaml
import os
import shutil
import schedule
import time
import subprocess
import sys
from crawler import Crawler
from argparse import ArgumentParser
from functools import partial
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, TimeoutError


import requests
from PIL import Image
from io import BytesIO

# 確保這裡使用的是正確的圖片直接鏈接
url =  "https://i.imgur.com/tEpqmeh.jpg"  # 這是示例，請確認此鏈接是有效的
url1 = "https://i.imgur.com/tEpqmeh.jpeg"  # 這是示例，請確認此鏈接是有效的


# https://imgur.com/8jMMXNE
# https://i.imgur.com/8jMMXNE.jpeg
# 發送請求下載圖片
response = requests.get(url)
if response.status_code == 200:
    # 將圖片保存為本地文件
    img = Image.open(BytesIO(response.content))
    img.save("downloaded_image.jpg")  # 本地保存的檔案名稱
    print("圖片已下載並保存為 downloaded_image.jpg")
else:
    print("無法下載圖片。請檢查 URL 是否正確。")




# https://imgur.com/5BIeBwJ
# https://imgur.com/tEpqmeh

