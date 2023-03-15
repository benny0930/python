import threading
from selenium.webdriver.common.by import By

# base = db = None


def start(_base, _db):
    global base, db
    try:
        base = _base
        db = _db

        # 網路美女
        t = threading.Thread(target=forum736, args=())
        t.start()  # 開始

    except Exception as e:
        base.sendTG(base.chat_id_test, str(e))

    return True



def forum736(): # 網路美女
    driver = base.defaultChrome()
    driver.get('https://www.jkforum.net/forum-736-1.html')
    driver.add_cookie({'name': 'over18', 'value': '1'})
    driver.get('https://www.jkforum.net/forum-736-1.html')
    chat_id = '-695426401'

    all_a = driver.find_elements(By.XPATH, '//ul[@id="waterfall"]/li/h3/a[1]')
    # print(len(all_a))
    try:
        for a in all_a:
            [url,title] = [a.get_attribute('href'), a.text]
            results = db.select(
                " SELECT id, name FROM fa_ptt WHERE `url` = '%s'" % (url))
            if len(results) < 1:
                sql = "INSERT INTO `fa_ptt` (`name`, `url`, `title`, `createtime`, `updatetime`) VALUES ('%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))" % ('Gamesale', url, title)
                db.insert(sql)

                base.sendTG(chat_id, '<pre>' + title + '</pre>' + url)

                driver1 = base.defaultChrome()
                try:
                    driver1.get(url)
                    driver1.add_cookie({'name': 'over18', 'value': '1'})
                    driver1.get(url)
                    all_img = driver1.find_elements(By.XPATH, '//ignore_js_op/img')
                    for img in all_img:
                        src = img.get_attribute('src')
                        base.send_photo(chat_id, src, '' )
                except Exception as e:
                    print(e)
                driver1.close()

    except Exception as e:
                base.sendTG(chat_id, str(e))

    driver.close()

