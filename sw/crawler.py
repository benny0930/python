# coding: utf-8
import asyncio
import simplejson as json
import inspect
import base64
import db
import random


from decimal import Decimal, InvalidOperation
from functools import partial
from playwright.async_api import async_playwright
from base import Base
from datetime import datetime

custom_loads = partial(json.loads, parse_float=Decimal)


class Crawler:
    def __init__(self, config, ):
        self._config: dict = config
        self.base = Base(config)
        self._db = db

    # ---------------

    def setup(self):
        pass

    async def run(self):
        tasks = []
        # usernames = ['big930{:02d}'.format(i) for i in range(1, 62)]
        usernames = ['big93031','big93035','big93056','big93057']
        for account in usernames:
            print()
            print(account)
            # 同時執行的任務數量
            concurrent_tasks = 1
            # 創建異步任務
            task = self.scrape_swag(account)
            tasks.append(task)

            # 當累積到指定數量的任務時，等待它們完成
            if len(tasks) == concurrent_tasks:
                await asyncio.gather(*tasks)
                tasks = []
        if len(tasks) > 0:
            await asyncio.gather(*tasks)

        # asyncio.run(self.scrape_swag())
        # asyncio.run(self.mailnesia_get_code("big93006"))
        # 8 9 10 12 13 14 15

    # ---------------

    # ---------------

    async def scrape_swag(self, account, index=0):
        async with async_playwright() as pw:
            try:
                browser = await pw.chromium.launch(headless=False)
                context = await browser.new_context()
                page = await context.new_page()

                # 禁用图片加载
                async def intercept_request(route, request):
                    if request.resource_type in ['image', 'media']:
                        await route.abort()
                    else:
                        await route.continue_()

                await page.route('**/*',
                                 lambda route, request: asyncio.ensure_future(intercept_request(route, request)))

                await page.goto('https://swag.live/settings?lang=zh-TW')
                await self.swag_login(page, account, account)
                # await page.wait_for_timeout(30 * 1000)
                if await self.swag_award(page, account):
                    await self.swag_money(page, account)
                    await browser.close()
                else:
                    await browser.close()
                    if index < 3:
                        await self.scrape_swag(account, index + 1)
            except Exception as e:
                print(f"{account} An error 1 on line {inspect.currentframe().f_lineno}: {e}")
                await browser.close()

    async def swag_login(self, page, username, password):
        try:
            print(f"{username} 開始登入")
            await page.click('text="登入/註冊"')
            await page.wait_for_timeout(2 * 1000)
            await page.click('button:has-text("登入")')
            await page.wait_for_timeout(2 * 1000)
            await page.type('input[name="username"]', username)
            await page.wait_for_timeout(1 * 1000)
            await page.type('input[name="password"]', password)
            await page.wait_for_timeout(1 * 1000)
            await page.click('button[type="submit"]:has-text("登入")')
            print(f"{username} 送出")
            await page.wait_for_timeout(5 * 1000)
        except Exception as e:
            await page.screenshot(path="sw.png")
            print(f"{username} An error 2 on line {inspect.currentframe().f_lineno}: {e}")

    async def swag_award(self, page, account):
        try:
            await page.goto('https://swag.live/following?lang=zh-TW')
            await page.wait_for_timeout(2 * 1000)

            await page.click('div[aria-label="背包"]')
            await page.wait_for_timeout(2 * 1000)

            button = await page.query_selector('button:has-text("已領取")')
            if button:
                print(f"{account} 已領取")
            else:
                print(f"{account} 送出領取")
                await page.click('button:has-text("免費")')
                await page.wait_for_timeout(5 * 1000)

                button_exists = await page.evaluate(
                    'Boolean([...document.querySelectorAll("button")].find(button => button.textContent.includes("寄送驗證信")))')

                if button_exists:
                    print(f"{account} 需要驗證")
                    await self.swag_verisy_new(page, account)
                    await self.swag_award(page, account)
            print(f"{account} 領取成功")
            # await page.click('img[alt="close"]/..')
            return True
        except Exception as e:
            print(f"{account} An error 5 on line {inspect.currentframe().f_lineno}: {e}")
            return False

        # await self.swag_money(page, account, False)

    async def swag_money(self, page, account, is_go_to=True):
        try:
            if is_go_to:
                await page.goto('https://swag.live/following?lang=zh-TW')
                await page.wait_for_timeout(2 * 1000)

            await page.click('button[aria-label="選單"]')
            await page.wait_for_timeout(3 * 1000)

            city_option_elements = await page.query_selector_all('img[alt="Diamond"]')
            parent_element = await city_option_elements[0].query_selector('xpath=..')
            diamond = (await parent_element.inner_text()).replace(',', '').replace('\n', '').replace('購買鑽石', '')
            print(f"{account} 鑽石數量:", diamond)

            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

            sql = "INSERT INTO fa_sw (name, m, createtime, updatetime, update_at) "
            sql += f"VALUES ('{account}', '{diamond}', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()), DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s'))"
            sql += "ON DUPLICATE KEY UPDATE "
            sql += f"m = '{diamond}' , update_at = DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s'), m_before = CONCAT(m, ',', m_before) ;"
            db.insert(sql)

        except Exception as e:
            print(f"{account} An error 6 on line {inspect.currentframe().f_lineno}: {e}")

    async def swag_verisy_new(self, page, account):
        try:
            await page.fill('input[name="email"]', '')  # 先清除
            await page.type('input[name="email"]', account + '@mailnesia.com')
            await page.wait_for_timeout(2 * 1000)
            await page.click('button:has-text("寄送驗證信")')
            await page.wait_for_timeout(10 * 1000)
            verification_code = await self.mailnesia_get_code(account)
            await page.wait_for_timeout(1 * 1000)
            await page.type('input[placeholder="6 位數代碼"]', verification_code)
            # await page.wait_for_timeout(2 * 1000)
            # await page.click('button:has-text("送出")')
            await page.wait_for_timeout(5 * 1000)
        except Exception as e:
            print(f"{account} An error 4 on line {inspect.currentframe().f_lineno}: {e}")

    async def mailnesia_get_code(self, account, index=0):
        verification_code = ""
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto('https://mailnesia.com/mailbox/' + account)

            try:
                text_content = await page.eval_on_selector(
                    'a.email:has-text("驗證您的電子郵件驗證碼")',
                    'link => link.textContent'
                )
                verification_code = text_content.split()[-1]
            except Exception as e:
                print(f"{account} An error 7 on line {inspect.currentframe().f_lineno}: {e}")
                if index < 3:
                    verification_code = self.mailnesia_get_code(account, index + 1)

            await browser.close()
            return verification_code

    async def swag_verisy(self, page, account):
        try:
            await page.goto('https://swag.live/manage-profile/account-linking?lang=zh-TW')
            await page.wait_for_timeout(2 * 1000)

            spans = await page.query_selector_all('span')
            verified_spans = [span for span in spans if "已驗證" in await span.inner_text()]

            if verified_spans:
                print("已驗證")
            else:
                await page.click('button:has-text("驗證電子郵件")')
                await page.wait_for_timeout(2 * 1000)
                await self.swag_verisy_new(page, account)
        except Exception as e:
            print(f"{account} An error 3 on line {inspect.currentframe().f_lineno}: {e}")
