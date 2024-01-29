# coding: utf-8
import inspect
import time

import db
from playwright.sync_api import sync_playwright
from base import Base
from datetime import datetime, timedelta


class Crawler:
    def __init__(self, config, ):
        self._config: dict = config
        self.base = Base(config)
        self._db = db
        self.is_test = True
        self.chat_id_image = "-1001932657196"  # 正式
        self.chat_id_money = "-1001647881084"  # 正式
        if (self.is_test):
            self.chat_id_image = "-1001911277875"
            self.chat_id_money = "-1001911277875"

    # ---------------

    def setup(self):
        pass

    def run(self, type):
        current_time = datetime.now()
        current_minute = current_time.minute
        print(f"{type} 開始執行: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.base.clear_images_folder()

        if (type == "PTT"):
            # 每 5 分鐘執行一次 ptt
            self.scrape_ptt("https://www.ptt.cc/bbs/Beauty/index.html", "Beauty", self.chat_id_image)
            self.scrape_ptt("https://www.ptt.cc/bbs/Gamesale/index.html", "Gamesale", self.chat_id_money)
            self.scrape_ptt("https://www.ptt.cc/bbs/Lifeismoney/index.html", "Lifeismoney", self.chat_id_money)
            self.scrape_ptt("https://www.ptt.cc/bbs/forsale/index.html", "forsale", self.chat_id_money)

        if (type == "clickme"):
            # 每小時爬 clickme
            self.scrape_clickme(self.chat_id_image)

        if (type == "delete"):
            self.base.url = []
            if (not self.is_test):
                sql = "DELETE FROM fa_ptt WHERE createtime < UNIX_TIMESTAMP(NOW() - INTERVAL 2 DAY);"
                db.delete(sql)

        print(f"{type} 執行結束: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # ---------------

    # ---------------

    def scrape_ptt(self, url, type, chat_id):
        href_list = []
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=(not self.is_test))
            context = browser.new_context()
            page = context.new_page()
            if (not self.is_test):
                page.set_viewport_size({"width": 1920, "height": 1080})
            try:
                page.goto(url)
                context.add_cookies([{'name': 'over18', 'value': '1', 'url': 'https://www.ptt.cc'}])
                page.goto(url)
                page.wait_for_load_state("load")

                # 提取所有標題連結
                links = page.query_selector_all('.title a')

                # 打印標題文本和連結
                for link in links:
                    title_text = link.inner_text()
                    href_value = link.get_attribute('href')

                    print(f"標題: {title_text}\n連結: {href_value}")

                    if title_text.find('公告') >= 0 or title_text.find('大尺碼') >= 0:
                        print(f'跳過\n')
                        continue

                    if href_value in self.base.url:
                        print(f'已存在(base)\n')
                        continue
                    self.base.url.append(href_value)
                    results = db.select(" SELECT id, name FROM fa_ptt WHERE `url` = '%s'" % (href_value))
                    if len(results) < 1:
                        href_list.append({'title': title_text, 'href': href_value})

                        # self.scrape_ptt_detail("Beauty", title_text, "https://www.ptt.cc" + href_value)
                    else:
                        print(f'已存在({results})\n')
                        continue
            except Exception as e:
                print(f"An error occurred on line {inspect.currentframe().f_lineno}: {e}")

            browser.close()

        print("開始列表" + str(len(href_list)))
        for pair in href_list:
            print(href_value)
            self.scrape_ptt_detail(type, chat_id, pair['title'], pair['href'])

    def scrape_ptt_detail(self, type, chat_id, title, url):
        print(f"爬取頁面內容 => 標題: {title}\n連結: {url}")

        with sync_playwright() as pw1:
            browser = pw1.chromium.launch(headless=(not self.is_test))
            context = browser.new_context()
            page = context.new_page()
            if (not self.is_test):
                page.set_viewport_size({"width": 1920, "height": 1080})
            try:
                if (not self.is_test):
                    sql = "INSERT INTO `fa_ptt` (`name`, `url`, `title`, `createtime`, `updatetime`) VALUES "
                    sql += "('%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))" % (type, url, title)
                    db.insert(sql)
                url = "https://www.ptt.cc/" + url
                page.goto(url)
                context.add_cookies([{'name': 'over18', 'value': '1', 'url': 'https://www.ptt.cc'}])
                page.goto(url)
                page.wait_for_load_state("load")

                # self.base.sendTG(self.chat_id_image, '<a href="' + url + '">' + title + '</a>')
                page.screenshot(path="python_ptt.png")
                with open("python_ptt.png", 'rb') as photo_file:
                    self.base.send_photo(chat_id, photo_file, '<a href="' + url + '">' + title + '</a>', True)

                if type == "Beauty":
                    all_links = page.query_selector_all('#main-content a')

                    send_links = []

                    for link in all_links:
                        href_value = link.get_attribute('href')
                        if href_value.find('www.ptt.cc') >= 0:
                            print(f'{href_value} => 跳過\n')
                            continue
                        send_links.append(href_value)

                    self.base.send_media_group(chat_id, send_links)

            except Exception as e:
                print(f"An error occurred on line {inspect.currentframe().f_lineno}: {e}")
            browser.close()

    def scrape_clickme(self, chat_id):
        url = "https://r18.clickme.net/c/new/1"
        href_list = []
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=(not self.is_test))
            context = browser.new_context()
            page = context.new_page()
            if (not self.is_test):
                page.set_viewport_size({"width": 1920, "height": 1080})
            try:
                page.goto(url)
                page.wait_for_load_state("load")
                try:
                    button = page.locator("#enter")
                    if "已滿18歲 進入" in button.inner_text():
                        button.click()
                        print("按鈕已點擊")
                except Exception as e:
                    print(f"出現錯誤: {e}")
                page.wait_for_load_state("load")
                elements = page.query_selector_all('.article-list-info-area')

                for element in elements:
                    # 获取标题文本
                    title_text = element.query_selector('div').inner_text()

                    href_value = element.evaluate('(element) => element.parentElement.getAttribute("href")')

                    print(f"標題: {title_text}\n連結: {href_value}\n")

                    if title_text.find('Steam') >= 0 or title_text.find('DLsite') >= 0 or title_text.find(
                            '裏番') >= 0 or title_text.find('黃遊') >= 0:
                        print(f'跳過\n')
                        continue

                    if href_value in self.base.url:
                        print(f'已存在(base)\n')
                        continue
                    self.base.url.append(href_value)
                    results = db.select(" SELECT id, name FROM fa_ptt WHERE `url` = '%s'" % (href_value))
                    if len(results) < 1:
                        href_list.append({'title': title_text, 'href': href_value})
                    else:
                        print(f'已存在({results})\n')
                        continue
            except Exception as e:
                print(f"An error occurred on line {inspect.currentframe().f_lineno}: {e}")

            browser.close()

        print("開始列表" + str(len(href_list)))
        for pair in href_list:
            print(href_value)
            self.scrape_clickme_detail("clickme", chat_id, pair['title'], pair['href'])

    def scrape_clickme_detail(self, type, chat_id, title, url):
        print(f"爬取頁面內容 => 標題: {title}\n連結: {url}")

        with sync_playwright() as pw1:
            browser = pw1.chromium.launch(headless=(not self.is_test))
            context = browser.new_context()
            page = context.new_page()
            if (not self.is_test):
                page.set_viewport_size({"width": 1920, "height": 1080})
            try:
                if (not self.is_test):
                    sql = "INSERT INTO `fa_ptt` (`name`, `url`, `title`, `createtime`, `updatetime`) VALUES "
                    sql += "('%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))" % (type, url, title)
                    db.insert(sql)
                url = "https:" + url
                page.goto(url)
                page.wait_for_load_state("load")
                try:
                    button = page.locator("#enter")
                    if "已滿18歲 進入" in button.inner_text():
                        button.click()
                        print("按鈕已點擊")
                except Exception as e:
                    print(f"出現錯誤: {e}")
                page.wait_for_load_state("load")

                # self.base.sendTG(self.chat_id_image, '<a href="' + url + '">' + title + '</a>')
                page.screenshot(path="python_ptt.png")
                with open("python_ptt.png", 'rb') as photo_file:
                    self.base.send_photo(chat_id, photo_file, '<a href="' + url + '">' + title + '</a>', True)

                send_links = []
                article_element = page.locator("#article-detail-content")
                images = article_element.locator('img').all()
                for image in images:
                    # 获取图像的 src 属性
                    image_src = "https:" + image.get_attribute('src')
                    print(f"圖片連結: {image_src}")
                    send_links.append(image_src)
                self.base.send_media_group(chat_id, send_links)

            except Exception as e:
                print(f"An error occurred on line {inspect.currentframe().f_lineno}: {e}")
            browser.close()
