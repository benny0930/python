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


class Base:
    url = []

    def __init__(self, config, ):
        self._config: dict = config
        self.bot = telegram.Bot(token='5652787798:AAHiBgILVoZG-pL55Me7XBJwODWPm7ho1BM')
    def send_media_group(self, _chat_id, _media=None):
        if _media is not None and len(_media) > 0:
            print(len(_media))
            images = []
            image_names = []
            for url_one in _media:
                try:
                    val = url_one.rsplit('.', 1)[1]
                    if val == 'gif':
                        # Send a gif
                        print("GIF : " + url_one)
                        self.sendDocument(self.chat_id_image, url_one, "")
                    elif val == 'jpg':
                        # Send a Picture
                        print("Picture : " + url_one)
                        if not os.path.exists('images'):
                            os.makedirs('images')
                        image_name = 'images/image_' + str(hashlib.md5(url_one.encode()).hexdigest()) + '.jpg'
                        self.check_image_format(url_one, image_name)
                        image_names.append(image_name)
                        image1 = open(image_name, 'rb')
                        images.append(InputMediaPhoto(image1))
                        image1.close()
                    else:
                        self.sendTG(_chat_id, url_one)

                    if len(images) == 9:
                        self.sendMediaGroup(_chat_id, images)
                        images = []
                except:
                    pass

            if len(images) > 0:
                self.sendMediaGroup(_chat_id, images)
            for name_one in image_names:
                self.remove_image(name_one)

    def sendDocument(self, _chat_id, _file_opened, _caption, index=0):
        global sleep_sec
        try:
            self.bot.sendDocument(chat_id=_chat_id, document=_file_opened, caption=_caption, parse_mode='html')
        except Exception as e:
            traceback.print_exc()  # 這會顯示詳細的異常信息，包括行數
            print(f"An error occurred: {str(e)}")
            try:
                if index < 3 and "Retry in" in str(e):
                    index_new = index + 1
                    numbers = [int(n) for n in re.findall('\d+', str(e))]
                    print("sleep " + str(numbers[0]) + " s")
                    sleep_sec = numbers[0]
                    time.sleep(numbers[0])
                    sleep_sec = 0
                    self.sendDocument(_chat_id, _file_opened, _caption, index_new)
            except:
                pass

    def check_image_format(self, url, name):
        response = requests.get(url)

        # 将图片转换为 JPG 格式
        img = Image.open(BytesIO(response.content))
        img = img.convert('RGB')

        # 保存图片为 JPG 格式
        img.save(name)

    def sendTG(self, _chat_id, _msg, index=0):
        global sleep_sec
        try:
            self.bot.sendMessage(chat_id=_chat_id, text=_msg, parse_mode='html')
        except Exception as e:
            traceback.print_exc()  # 這會顯示詳細的異常信息，包括行數
            print(f"An error occurred: {str(e)}")
            try:
                if index < 3 and "Retry in" in str(e):
                    index_new = index + 1
                    numbers = [int(n) for n in re.findall('\d+', str(e))]
                    print("sleep " + str(numbers[0]) + " s")
                    sleep_sec = numbers[0]
                    time.sleep(numbers[0])
                    sleep_sec = 0
                    self.sendTG(_chat_id, _msg, index_new)
            except:
                pass

    def sendMediaGroup(self, _chat_id, _images, index=0):
        global sleep_sec
        try:
            print("發送數量：" + str(len(_images)))
            self.bot.send_media_group(chat_id=_chat_id, media=_images)
        except Exception as e:
            traceback.print_exc()  # 這會顯示詳細的異常信息，包括行數
            print(f"An error occurred: {str(e)}")
            try:
                if index < 3 and "Retry in" in str(e):
                    index_new = index + 1
                    numbers = [int(n) for n in re.findall('\d+', str(e))]
                    print("sleep " + str(numbers[0]) + " s")
                    sleep_sec = numbers[0]
                    time.sleep(numbers[0])
                    sleep_sec = 0
                    self.sendMediaGroup(_chat_id, _images, index_new)
            except:
                pass

    def remove_image(self, name_one):
        try:
            os.remove(name_one)
        except Exception as e:
            traceback.print_exc()  # 這會顯示詳細的異常信息，包括行數
            print(f"An error occurred: {str(e)}")
            time.sleep(1)
            self.remove_image(name_one)

    def clear_images_folder(self):
        images_folder = 'images'

        # 检查文件夹是否存在
        if not os.path.exists(images_folder):
            print(f"The folder '{images_folder}' does not exist.")
            return

        # 清空文件夹
        for filename in os.listdir(images_folder):
            file_path = os.path.join(images_folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                traceback.print_exc()  # 這會顯示詳細的異常信息，包括行數
                print(f"An error occurred: {str(e)}")

    def send_photo(self, _chat_id, _file_opened, _caption="", isPhoto=False):
        val = ""
        if not isPhoto:
            val = _file_opened.rsplit('.', 1)[1]
        if val == 'gif':
            # Send a gif
            # bot.sendDocument(chat_id=_chat_id, document=_file_opened, caption=_caption, parse_mode='html')
            self.sendDocument(_chat_id, _file_opened, _caption)
        else:
            # Send a Picture
            self.sendPhoto(_chat_id, _file_opened, _caption)

    def sendPhoto(self, _chat_id, _file_opened, _caption, index=0):
        global sleep_sec
        try:
            self.bot.sendPhoto(chat_id=_chat_id, photo=_file_opened, caption=_caption, parse_mode='html')
        except Exception as e:
            print(str(e))
            try:
                if index < 3 and "Retry in" in str(e):
                    index_new = index + 1
                    numbers = [int(n) for n in re.findall('\d+', str(e))]
                    print("sleep " + str(numbers[0]) + " s")
                    sleep_sec = numbers[0]
                    time.sleep(numbers[0])
                    sleep_sec = 0
                    self.sendPhoto(_chat_id, _file_opened, _caption, index_new)
            except:
                pass

