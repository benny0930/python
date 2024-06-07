# coding: utf-8
import time
import os
import hashlib
import requests
import re
import telegram
import traceback
from telegram import InputMediaPhoto
from PIL import Image
from io import BytesIO
import sys
import base64
import json
from downloads import download

bot = telegram.Bot(token='5652787798:AAHiBgILVoZG-pL55Me7XBJwODWPm7ho1BM')

def check_image_format(url, name):
    try:
        print([url, name])
        download(url, out_path=name)
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as e:
        print(f"An error occurred: {e}")



def sendMediaGroup(_chat_id, _images, index=0):
    try:
        print(f"發送數量：{len(_images)}")
        bot.send_media_group(chat_id=_chat_id, media=_images)
    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred: {str(e)}")
        try:
            if index < 3 and "Retry in" in str(e):
                index_new = index + 1
                numbers = [int(n) for n in re.findall('\d+', str(e))]
                print(f"sleep {numbers[0]} s")
                time.sleep(numbers[0])
                sendMediaGroup(_chat_id, _images, index_new)
        except:
            pass


try:
    url_one = "https://i.meee.com.tw/efExhlV.png"

    if "meee.com" in url_one:
        print("YYY")
    else:
        print("NNN")

    if not os.path.exists('images'):
        os.makedirs('images')

    print(f"Picture: {url_one}")
    image_name = f'images/image_{hashlib.md5(url_one.encode()).hexdigest()}.jpg'
    images = []
    image_names = []

    # # 尝试下载并处理图片
    # check_image_format(url_one, image_name)
    #
    # # 确保文件确实存在且有效
    # if os.path.exists(image_name):
    #     with open(image_name, 'rb') as image_file:
    #         images.append(InputMediaPhoto(image_file))

    images.append(InputMediaPhoto(url_one))
    images.append(InputMediaPhoto(url_one))
    images.append(InputMediaPhoto(url_one))
    images.append(InputMediaPhoto(url_one))
    images.append(InputMediaPhoto(url_one))
    images.append(InputMediaPhoto(url_one))

    # 发送图片
    # sendMediaGroup("-1001911277875", images)
except Exception as e:
    print(f"An error occurred: {e}")
#
#
#
# import requests
#
