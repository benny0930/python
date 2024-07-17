# coding: utf-8
import inspect
import time

import db
import json
import re
import requests

from playwright.sync_api import sync_playwright
from base import Base
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime
from PTTLibrary import PTT
import sys


class Crawler:
    def __init__(self, config, ):
        self._config: dict = config
        self.base = Base(config)
        self._db = db
        self.is_test = config['is_test']
        self.chat_id_image = "-1001932657196"  # 正式
        self.chat_id_money = "-1001647881084"  # 正式
        self.chat_id_currency = "-1002100758150"  # 正式
        self.chat_id_game = "-4259391320"
        if (self.is_test):
            self.chat_id_image = "-1001911277875"
            self.chat_id_money = "-1001911277875"
            self.chat_id_currency = "-1001911277875"
            self.chat_id_game = "-1001911277875"

    # ---------------

    def setup(self):
        pass

    def run(self, type):
        try:

            if (type == "TEST"):
                self.base.sendTG(self.chat_id_game, "msg_sendTG")
                return

            current_time = datetime.now()
            current_minute = current_time.minute
            print(f"{type} 開始執行: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            self.base.clear_images_folder()

            if (type == "PTT"):
                self.scrape_ptt("https://www.ptt.cc/bbs/Beauty/index.html", "Beauty", self.chat_id_image)
                self.scrape_ptt("https://www.ptt.cc/bbs/Gamesale/index.html", "Gamesale", self.chat_id_game)
                self.scrape_ptt("https://www.ptt.cc/bbs/Lifeismoney/index.html", "Lifeismoney", self.chat_id_money)
                self.scrape_ptt("https://www.ptt.cc/bbs/forsale/index.html", "forsale", self.chat_id_money)

            if (type == "clickme"):
                self.scrape_clickme(self.chat_id_image)

            if (type == "happy"):
                self.scrape_happy()

            if (type == "51"):
                self.scrape_51(self.chat_id_image)
                # self.scrape_51_detail(type, self.chat_id_image, "111", "https://www.51cg1.com/archives/126502/")

            if (type == "currency"):
                self.currency(self.chat_id_currency)

            if (type == "pttLogin"):
                self.pttLogin(self.chat_id_currency)

            if (type == "delete"):
                self.base.url = []
                if (not self.is_test):
                    sql = "DELETE FROM fa_ptt WHERE createtime < UNIX_TIMESTAMP(NOW() - INTERVAL 2 DAY);"
                    db.delete(sql)
        except:
            self.base.sendTG(self.chat_id_currency, type + " error : " + sys.exc_info())
        print(f"{type} 執行結束: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # ---------------
    def get_proxy(self):
        url = 'http://172.104.85.146'  # X1
        port = 3128
        return f'{url}:{port}'

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

                if (self.is_test):
                    print(type)

                if type == "Beauty":
                    all_links = page.query_selector_all('#main-content a')
                    if (self.is_test):
                        print(all_links)
                    send_links = []

                    for link in all_links:
                        href_value = link.get_attribute('href')
                        if (self.is_test):
                            print(href_value)
                        if href_value.find('www.ptt.cc') >= 0:
                            print(f'{href_value} => 跳過\n')
                            continue
                        send_links.append(href_value)
                    if (self.is_test):
                        print(send_links)
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

    def scrape_happy(self):

        with sync_playwright() as pw:
            # proxy = self.get_proxy()
            browser = pw.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            for i in range(1, 21):

                url = "https://m.happymh.com/apis/u/myBookcase"
                url += "?token=BD4BBB0F-F826-4F83-A2FF-E28390EFA8BF"
                url += "&p=" + str(i)
                url += "&order_type=order_last_date"

                # 前往目标页面
                print(url)
                page.goto(url)  # 替换成你要访问的网址

                # 获取页面内容
                page_content = page.content()

                json_data_match = re.search(r'{"status":.*}', page_content)

                if json_data_match:
                    json_data = json_data_match.group()

                    # 尝试解析JSON内容
                    try:
                        data = json.loads(json_data)
                        if "data" in data and "list" in data["data"]:
                            data_list = data["data"]["list"]
                            if data_list:
                                for item in data_list:
                                    print("--------------------")
                                    name = item["serie_name"]
                                    read_name = item["read_chapter_name"]
                                    last_name = item["last_chapter_name"]
                                    href_value = "https://m.happymh.com/manga/" + item["serie_code"]
                                    print([name, read_name, last_name, url])
                                    results = db.select(
                                        " SELECT id, name, new_episode FROM fa_comic WHERE `url` = '%s'" % (href_value))
                                    if len(results) < 1:
                                        print("不存在")
                                        sql = "INSERT INTO `fa_comic` (`name`, `url`, `last_episode`, `new_episode`, `website`, `active`, `new`, `createtime`, `updatetime`) VALUES "
                                        sql += "('%s', '%s', '%s', '%s', 'happy', 'Y', 'Y', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))" % (
                                            name, href_value, read_name, last_name)
                                        db.insert(sql)
                                    else:
                                        comic_id, existing_name, existing_new_episode = results[0]
                                        print([comic_id, existing_name, existing_new_episode])
                                        if last_name != existing_new_episode:  # 網站最新 != DB最新
                                            new = "Y"
                                            if read_name == last_name:  # 網站已讀 == 網站最新
                                                new = "N"
                                            sql = "UPDATE `fa_comic` SET `last_episode` = '" + read_name + "', `new_episode` = '" + last_name + "', `new` = '" + new + "', `updatetime` = UNIX_TIMESTAMP(NOW()) WHERE `id` = '" + str(
                                                comic_id) + "'"
                                            db.insert(sql)
                                            print(f'已更新 (ID: {comic_id})')
                                        else:  # 網站最新 = DB 最新
                                            if read_name != existing_name:  # 網站已讀 != DB 已讀
                                                new = "Y"
                                                if read_name == last_name:  # 網站已讀 == 網站最新
                                                    new = "N"
                                                sql = "UPDATE `fa_comic` SET `last_episode` = '" + read_name + "', `new_episode` = '" + last_name + "', `new` = '" + new + "', `updatetime` = UNIX_TIMESTAMP(NOW()) WHERE `id` = '" + str(
                                                    comic_id) + "'"
                                                db.insert(sql)
                                            print(f'已存在 (ID: {comic_id})')
                                    print("-------------------- end ")
                            else:
                                print("列表中没有数据")
                                break
                        else:
                            print("数据中不存在list或data")
                            break
                    except json.JSONDecodeError:
                        print("无法解析JSON内容")
                        break
                else:
                    print("未找到JSON数据")
                    break
            browser.close()

    def scrape_51(self, chat_id):
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
            self.scrape_51_detail("51", chat_id, pair['title'], pair['href'])

    def currency_240607(self, chat_id):

        now = datetime.now()
        formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        msg_sendTG = "<pre>pre-formatted fixed-width code block</pre>"

        url = "https://www.okx.com/v3/c2c/otc-ticker/quotedPrice"
        params = {
            "side": "buy",
            "quoteCurrency": "TWD",
            "baseCurrency": "USDT"
        }
        response = self.base.api_get(url, params)
        money_usdt_to_twd = response['data'][0]['price']
        # print("USDT to TWD:", money_usdt_to_twd)
        # msg_sendTG = msg_sendTG + "<p>USDT轉台幣匯率為: "+money_usdt_to_twd+"</p>"
        msg_sendTG = '<blockquote><b>USDT轉台幣匯率為</b>: ' + money_usdt_to_twd + '</blockquote>'

        total_profit_USDT = 0
        total_profit_TWD = 0
        results = db.select(" SELECT name, quantity, cost FROM fa_currency WHERE 1 ")
        for row in results:
            name, quantity, cost = row
            # https://min-api.cryptocompare.com/data/price?fsym='+name+'&tsyms=USDT
            url = "https://min-api.cryptocompare.com/data/price"
            params = {
                "fsym": name,
                "tsyms": "USDT",
            }
            response = self.base.api_get(url, params)
            USDT = response['USDT']
            msg_sendTG += '<blockquote>'
            msg_sendTG += '<b>幣種</b>: ' + name + '\n'
            msg_sendTG += '<b>數量</b>: ' + quantity + '\n'
            msg_sendTG += '<b>成本</b>: ' + cost + '\n'
            msg_sendTG += '<b>時價</b>: ' + str(USDT) + '\n'
            profit_USDT = round((float(USDT) - float(cost)) * float(quantity), 2)
            total_profit_USDT += profit_USDT
            profit_TWD = round(profit_USDT * float(money_usdt_to_twd), 2)
            total_profit_TWD += profit_TWD
            msg_sendTG += '<b>盈虧(USDT)</b>: ' + str(profit_USDT) + '\n'
            msg_sendTG += '<b>盈虧(TWD)</b>: ' + str(profit_TWD) + '\n'
            msg_sendTG += '</blockquote>'

        msg_sendTG += '<blockquote>'
        msg_sendTG += '<b>總盈虧(USDT)</b>: ' + str(total_profit_USDT) + '\n'
        msg_sendTG += '<b>總盈虧(TWD)</b>: ' + str(total_profit_TWD) + '\n'
        msg_sendTG += '</blockquote>'

        self.base.sendTG(chat_id, msg_sendTG)

    def currency(self, chat_id):
        url = "https://api.coinbase.com/v2/exchange-rates?currency=USDT"
        params = {}
        response = self.base.api_get(url, params)
        money_usdt_to_twd = response['data']['rates']['TWD']
        msg_sendTG = '<blockquote><b>USDT轉台幣匯率為</b>: ' + money_usdt_to_twd + '</blockquote>'

        total_profit_USDT = 0
        total_profit_TWD = 0
        results = db.select(" SELECT name, quantity, cost FROM fa_currency WHERE 1 ")
        for row in results:
            name, quantity, cost = row
            url = "https://api.coinbase.com/v2/exchange-rates?currency=" + str(name)
            params = {}
            response = self.base.api_get(url, params)
            money_to_USDT = response['data']['rates']['USD']
            msg_sendTG += '<blockquote>'
            msg_sendTG += '<b>幣種</b>: ' + name + '\n'
            msg_sendTG += '<b>數量</b>: ' + quantity + '\n'
            msg_sendTG += '<b>成本</b>: ' + cost + '\n'
            msg_sendTG += '<b>時價</b>: ' + str(money_to_USDT) + '\n'
            profit_USDT = round((float(money_to_USDT) - float(cost)) * float(quantity), 2)
            total_profit_USDT += profit_USDT
            profit_TWD = round(profit_USDT * float(money_usdt_to_twd), 2)
            total_profit_TWD += profit_TWD
            msg_sendTG += '<b>盈虧(USDT)</b>: ' + str(profit_USDT) + '\n'
            msg_sendTG += '<b>盈虧(TWD)</b>: ' + str(profit_TWD) + '\n'
            msg_sendTG += '</blockquote>'

        msg_sendTG += '<blockquote>'
        msg_sendTG += '<b>總盈虧(USDT)</b>: ' + str(total_profit_USDT) + '\n'
        msg_sendTG += '<b>總盈虧(TWD)</b>: ' + str(total_profit_TWD) + '\n'
        msg_sendTG += '</blockquote>'

        self.base.sendTG(chat_id, msg_sendTG)

    def pttLogin(self, chat_id):

        for pt in self._config['ptt_account']:
            ID = pt['account']
            Password = str(pt['password'])
            print(ID)
            PTTBot = PTT.Library()
            PTTBot.login(ID, Password)
            PTTBot.logout()

    def scrape_51_detail(self, type, chat_id, title, url):
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
                page.goto(url)
                # self.base.sendTG(self.chat_id_image, '<a href="' + url + '">' + title + '</a>')
                page.screenshot(path="python_ptt.png")
                with open("python_ptt.png", 'rb') as photo_file:
                    self.base.send_photo(chat_id, photo_file, '<a href="' + url + '">' + title + '</a>', True)
                no_send_links = []
                send_links = []
                archive = page.wait_for_selector(".post-content")
                images = archive.query_selector_all("img")

                # 获取 div.article-bottom-apps 内部的 img 元素
                article_bottom_apps = archive.query_selector(".article-bottom-apps")
                if article_bottom_apps:
                    bottom_images = set(article_bottom_apps.query_selector_all("img"))
                else:
                    bottom_images = set()
                for image in bottom_images:
                    no_send_links.append(image.get_attribute('src'))

                for image in images:
                    # 获取图像的 src 属性
                    image_src = image.get_attribute('src')
                    if image_src not in no_send_links:
                        send_links.append(image_src)
                self.base.send_media_group(chat_id, send_links)

            except Exception as e:
                print(f"An error occurred on line {inspect.currentframe().f_lineno}: {e}")
            browser.close()
