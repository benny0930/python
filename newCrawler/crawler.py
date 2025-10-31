# coding: utf-8
import inspect
import db
import json
import re
import time

from base import Base
from datetime import datetime
from PTTLibrary import PTT
from playwright.sync_api import sync_playwright


class Crawler:

    def __init__(self, config, ):
        self.is_test = config['is_test']
        self._config: dict = config
        self.base = Base(config)
        self._db = db

    # ---------------

    def run(self, type):
        current_time = datetime.now()
        print(f"{type} 開始執行: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        try:
            if type == "TEST":
                img_path = r"C:\Code\benny\python\newCrawler\python_ptt.png"
                img_url = self.base.upload_to_laptop_up(img_path)
                print(img_url)

            else:
                self.base.clear_images_folder()
                type_actions = {
                    "delete": lambda: self.handle_delete(),
                    "pttLogin": lambda: self.pttLogin(),
                    "PTT": lambda: [
                        self.scrape_ptt("https://www.ptt.cc/bbs/Beauty/index.html", "Beauty"),
                        self.scrape_ptt("https://www.ptt.cc/bbs/Gamesale/index.html", "Gamesale"),
                        self.scrape_ptt("https://www.ptt.cc/bbs/Lifeismoney/index.html", "Lifeismoney"),
                        self.scrape_ptt("https://www.ptt.cc/bbs/forsale/index.html", "forsale")
                    ],
                    "clickme": lambda: self.scrape_clickme(''),
                    "clickme18": lambda: self.scrape_clickme('18'),
                    "51": lambda: self.scrape_51(),
                    "avjoy": lambda: self.avjoy(),
                }

                if type in type_actions:
                    type_actions[type]()
                else:
                    print(f"Unsupported type: {type}")

        except Exception as e:
            print(f"{type} error: {str(e)}")

        print(f"{type} 執行結束: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def handle_delete(self):
        self.base.url = []
        if not self.is_test:
            two_days_ago = int(time.time()) - 2 * 24 * 60 * 60
            db.handle_delete(two_days_ago)
            self.base.delete_to_laptop_up(3)

    # ---------------

    def scrape_ptt(self, url, type):
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

                    if href_value in self.base.url:
                        print(f'已存在(base)\n')
                        continue
                    self.base.url.append(href_value)

                    if title_text.find('公告') >= 0 or title_text.find('大尺碼') >= 0:
                        print(f'跳過\n')
                        continue

                    if type == "Gamesale" and title_text.find('NS') < 0:
                        print(f'Gamesale 非 NS 跳過\n')
                        continue

                    results = db.select_fa_ptt(href_value)
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
            self.scrape_ptt_detail(type, pair['title'], pair['href'])

    def scrape_ptt_detail(self, type, title, url):
        print(f"爬取頁面內容 => 標題: {title}\n連結: {url}")

        with sync_playwright() as pw1:
            browser = pw1.chromium.launch(headless=(not self.is_test))
            context = browser.new_context()
            page = context.new_page()
            if (not self.is_test):
                page.set_viewport_size({"width": 1920, "height": 1080})
            try:
                ptt_id = 0
                if (not self.is_test):
                    ptt_id = db.insert_fa_ptt(type, url, title)
                url = "https://www.ptt.cc/" + url
                print(url)
                page.goto(url)
                context.add_cookies([{'name': 'over18', 'value': '1', 'url': 'https://www.ptt.cc'}])
                page.goto(url)
                page.wait_for_load_state("load")

                page.screenshot(path="python_ptt.png")
                img_url = self.base.upload_to_laptop_up("python_ptt.png")
                print(img_url)
                is_follow = int(self.base.contains_video_key(title))
                main_id = db.insert_fa_ptt_main(ptt_id, title, type, img_url, is_follow)

                if (self.is_test):
                    print(type)

                if type == "Beauty":
                    all_links = page.query_selector_all('#main-content a')
                    if (self.is_test):
                        print(all_links)

                    for link in all_links:
                        href_value = link.get_attribute('href')
                        if (self.is_test):
                            print(href_value)
                        if href_value.find('www.ptt.cc') >= 0:
                            print(f'{href_value} => 跳過\n')
                            continue
                        db.insert_fa_ptt_images(main_id, href_value)

            except Exception as e:
                print(f"An error occurred on line {inspect.currentframe().f_lineno}: {e}")
                if (self.is_test):
                    exit(1)
            browser.close()

    def scrape_clickme(self, type):
        if type == '18':
            url = "https://r18.clickme.net/c/new/1"
        else:
            url = "https://clickme.net/c/beauty"
        href_list = []
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=(not self.is_test))
            context = browser.new_context()
            page = context.new_page()
            if (not self.is_test):
                page.set_viewport_size({"width": 1920, "height": 1080})
            try:
                page.goto(url)
                if type == '18':
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
                    results = db.select_fa_ptt(href_value)
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
            if type == '18':
                self.scrape_clickme_detail("clickme18", pair['title'], pair['href'], type)
            else:
                self.scrape_clickme_detail("clickme", pair['title'], pair['href'], type)

    def scrape_clickme_detail(self, type, title, url, is18):
        print(f"爬取頁面內容 => 標題: {title}\n連結: {url}")

        with sync_playwright() as pw1:
            browser = pw1.chromium.launch(headless=(not self.is_test))
            context = browser.new_context()
            page = context.new_page()
            if (not self.is_test):
                page.set_viewport_size({"width": 1920, "height": 1080})
            try:
                ptt_id = 0
                if (not self.is_test):
                    ptt_id = db.insert_fa_ptt(type, url, title)
                url = "https:" + url
                page.goto(url)
                if is18 == '18':
                    page.wait_for_load_state("load")
                    try:
                        button = page.locator("#enter")
                        if "已滿18歲 進入" in button.inner_text():
                            button.click()
                            print("按鈕已點擊")
                    except Exception as e:
                        print(f"出現錯誤: {e}")
                    page.wait_for_load_state("load")

                page.screenshot(path="python_ptt.png")
                img_url = self.base.upload_to_laptop_up("python_ptt.png")
                print(img_url)
                is_follow = int(self.base.contains_video_key(title))
                main_id = db.insert_fa_ptt_main(ptt_id, title, type, img_url, is_follow)

                send_links = []
                article_element = page.locator("#article-detail-content")
                images = article_element.locator('img').all()
                for image in images:
                    # 获取图像的 src 属性
                    image_src = "https:" + image.get_attribute('src')
                    db.insert_fa_ptt_images(main_id, image_src)

            except Exception as e:
                print(f"An error occurred on line {inspect.currentframe().f_lineno}: {e}")
            browser.close()

    def scrape_51(self):
        base_url = 'https://www.51cg1.com'
        href_list = []
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=(not self.is_test))
            context = browser.new_context()
            page = context.new_page()
            if (not self.is_test):
                page.set_viewport_size({"width": 1920, "height": 1080})
            try:
                page.goto(base_url + "/category/wpcz/")
                page.wait_for_load_state("load")
                archive = page.wait_for_selector("#archive")
                elements = archive.query_selector_all("a")

                for element in elements:

                    title_element = element.query_selector("h2")
                    if not title_element:
                        continue

                    title_text = title_element.inner_text()
                    href_value = element.get_attribute("href")
                    if "category" in href_value:
                        print(f'跳過\n')
                        continue

                    href_value = base_url + href_value

                    print(f"標題: {title_text}\n連結: {href_value}\n")

                    if href_value in self.base.url:
                        print(f'已存在(base)\n')
                        continue
                    self.base.url.append(href_value)
                    results = db.select_fa_ptt(href_value)
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
            self.scrape_51_detail("51", pair['title'], pair['href'])

    def scrape_51_detail(self, type, title, url):
        print(f"爬取頁面內容 => 標題: {title}\n連結: {url}")

        with sync_playwright() as pw1:
            browser = pw1.chromium.launch(headless=(not self.is_test))
            context = browser.new_context()
            page = context.new_page()
            if (not self.is_test):
                page.set_viewport_size({"width": 1920, "height": 1080})
            try:
                ptt_id = 0
                if (not self.is_test):
                    ptt_id = db.insert_fa_ptt(type, url, title)
                page.goto(url)
                time.sleep(3)
                try:
                    page.locator("#wanrningconfirm").click()
                except Exception as e:
                    print(f"出現錯誤: {e}")

                page.screenshot(path="python_ptt.png")
                img_url = self.base.upload_to_laptop_up("python_ptt.png")
                if (not img_url):
                    return

                is_follow = int(self.base.contains_video_key(title))
                main_id = db.insert_fa_ptt_main(ptt_id, title, type, img_url, is_follow)

                archive = page.wait_for_selector(".post-content")
                images = archive.query_selector_all("img")

                # 获取 div.article-bottom-apps 内部的 img 元素
                # 先把不想發送的底部圖片收集起來
                article_bottom_apps = archive.query_selector(".article-bottom-apps")
                if article_bottom_apps:
                    bottom_images = set(article_bottom_apps.query_selector_all("img"))
                else:
                    bottom_images = set()

                no_send_links = []
                for image in bottom_images:
                    no_send_links.append(image.get_attribute('src'))

                for image in images:
                    # 获取图像的 src 属性
                    image_src = image.get_attribute('src')
                    if image_src not in no_send_links:
                        local_path = self.base.save_image_to_file(image_src, "python_ptt.png")
                        if not local_path:
                            continue
                        # 上傳
                        img_url = self.base.upload_to_laptop_up(local_path)
                        if not img_url:
                            continue
                        db.insert_fa_ptt_images(main_id, img_url)

            except Exception as e:
                print(f"An error occurred on line {inspect.currentframe().f_lineno}: {e}")
            browser.close()

    def pttLogin(self):

        for pt in self._config['ptt_account']:
            ID = pt['account']
            Password = str(pt['password'])
            print(ID)
            PTTBot = PTT.Library()
            PTTBot.login(ID, Password)
            PTTBot.logout()

    def avjoy(self):
        base_url = 'https://avjoy.me'
        href_list = []
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=(not self.is_test))
            context = browser.new_context()
            page = context.new_page()
            if (not self.is_test):
                page.set_viewport_size({"width": 1920, "height": 1080})
            try:
                results = []
                page.goto(base_url + "/videos?page=1")

                # 選取所有的 content-row
                rows = page.query_selector_all("div.content-left div.row.content-row div")
                print(f"找到 {len(rows)} 筆資料")
                # page.screenshot(path="python_ptt.png")
                # with open("python_ptt.png", 'rb') as photo_file:
                #     self.base.send_photo(chat_id, photo_file, '<a href="' + "222" + '">' + "111" + '</a>', True)
                for row in rows:
                    link = row.query_selector("a")
                    img = row.query_selector("a img")

                    if link and img:
                        href = link.get_attribute("href")
                        img_src = img.get_attribute("src")
                        img_title = img.get_attribute("title")

                        print(f"標題: {img_title}\n連結: {href}\n")
                        href_value = "" + href
                        if href_value in self.base.url:
                            print(f'已存在(base)\n')
                            continue
                        self.base.url.append(href_value)

                        db_results = db.select_fa_ptt(href_value)
                        if len(db_results) < 1:
                            results.append({
                                "href": href,
                                "img_src": img_src,
                                "title": img_title
                            })
                        else:
                            print(f'已存在({db_results})\n')
                            continue
                browser.close()

                print("開始detail")

                for item in results:
                    print("------------------")
                    print(item)
                    url = item["href"]
                    title = item["title"]
                    found = self.base.contains_video_key(title)
                    if found:
                        browser = pw.chromium.launch(headless=(not self.is_test))
                        context = browser.new_context()
                        page = context.new_page()
                        if (not self.is_test):
                            page.set_viewport_size({"width": 1920, "height": 1080})
                        try:
                            ptt_id = 0

                            if (not self.is_test):
                                ptt_id = db.insert_fa_ptt("avjoy", url, title)

                            page.goto(base_url + url)

                            page.wait_for_selector('div.vjs-poster')

                            poster_element = page.query_selector('div.vjs-poster')
                            poster_element.screenshot(path="python_ptt.png")
                            img_url = self.base.upload_to_laptop_up("python_ptt.png")
                            is_follow = int(self.base.contains_video_key(title))
                            main_id = db.insert_fa_ptt_main(ptt_id, title, "avjoy", img_url, is_follow)

                        except Exception as e:
                            print(f"An error occurred on line {inspect.currentframe().f_lineno}: {e}")
                        browser.close()
                    else:
                        print(f"Item {item} is not in the video_key array.")

                    # # 原始圖片 URL
                    # image_url = item["img_src"]
                    #
                    # # 解析圖片 URL，將 .jpg 改為 .webm
                    # video_url = image_url.rsplit('/', 1)[0] + "/video.webm"  # 去掉圖片的文件名並加上 video.webm
                    #
                    # print(f"視頻 URL: {video_url}")
                    # self.base.sendDocument(chat_id, video_url, "")
                    # return
                    #
                    # self.base.send_photo(chat_id, item["img_src"], '<a href="' + item["href"] + '">' + item["img_title"] + '</a>', False)
            except Exception as e:
                print(f"An error occurred on line {inspect.currentframe().f_lineno}: {e}")
