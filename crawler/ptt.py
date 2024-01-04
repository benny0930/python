import threading
import time

from selenium.webdriver.common.by import By


# base = db = None


def set(_base, _db):
    global base, db
    base = _base
    db = _db


def start(_base, _db, index=0):
    set(_base, _db)
    try:

        ClickMe18()
        return

        # 看板 Beauty
        title = 'Beauty'
        results = db.select(" SELECT id, title, is_active, val FROM fa_is_open WHERE `title` = '%s'" % (title))
        [id, title, is_active, val] = results[0]
        if is_active == 'Y' and index % int(val) == 0:
            Beauty()
            # t = threading.Thread(target=Beauty, args=())
            # print("---------------")
            # print("Beauty Start")
            # t.start()  # 開始
            # t.join(600)

        # 看板 Gamesale
        title = 'Gamesale'
        results = db.select(" SELECT id, title, is_active, val FROM fa_is_open WHERE `title` = '%s'" % (title))
        [id, title, is_active, val] = results[0]
        if is_active == 'Y' and index % int(val) == 0:
            print("---------------")
            print("Gamesale Start")
            Gamesale()
            # t = threading.Thread(target=Gamesale, args=())
            # t.start()  # 開始
            # t.join(600)

        # 看板 Lifeismoney
        title = 'Lifeismoney'
        results = db.select(" SELECT id, title, is_active, val FROM fa_is_open WHERE `title` = '%s'" % (title))
        [id, title, is_active, val] = results[0]
        if is_active == 'Y' and index % int(val) == 0:
            print("---------------")
            print("Lifeismoney Start")
            Lifeismoney()
            # t = threading.Thread(target=Lifeismoney, args=())
            # t.start()  # 開始
            # t.join(600*4)

        # 看板 forsale
        title = 'forsale'
        results = db.select(" SELECT id, title, is_active, val FROM fa_is_open WHERE `title` = '%s'" % (title))
        [id, title, is_active, val] = results[0]
        if is_active == 'Y' and index % int(val) == 0:
            print("---------------")
            print("forsale Start")
            forsale()
            # t = threading.Thread(target=forsale, args=())
            # t.start()  # 開始
            # t.join(600*4)

        # https://nungvl.net/
        # title = 'Nungvl'
        # results = db.select(" SELECT id, title, is_active, val FROM fa_is_open WHERE `title` = '%s'" % (title))
        # [id, title, is_active, val] = results[0]
        # if is_active == 'Y' and index % int(val) == 0:
        #     print("---------------")
        #     print("Nungvl Start")
        #     # base.sendTG(base.chat_id_test, 'Nungvl Start')
        #     t = threading.Thread(target=Nungvl, args=())
        #     t.start()  # 開始
        #     t.join(600)

        # http://www.playno1.com/portal.php?mod=list&catid=78
        # title = 'Playno1'
        # results = db.select(" SELECT id, title, is_active, val FROM fa_is_open WHERE `title` = '%s'" % (title))
        # [id, title, is_active, val] = results[0]
        # if is_active == 'Y' and index % int(val) == 0:
        #     # base.sendTG(base.chat_id_test, 'Playno1 Start')
        #     t = threading.Thread(target=Playno1, args=())
        #     t.start()  # 開始

        # https://clickme.net/c/beauty
        title = 'clickme'
        results = db.select(" SELECT id, title, is_active, val FROM fa_is_open WHERE `title` = '%s'" % (title))
        [id, title, is_active, val] = results[0]
        if is_active == 'Y' and index % int(val) == 0:
            print("---------------")
            print("clickme Start")
            ClickMe()

    except Exception as e:
        base.sendTG(base.chat_id_test, str(e))

    return True


def Beauty():
    driver = base.defaultChrome()
    driver.get('https://www.ptt.cc/bbs/Beauty/index.html')
    driver.add_cookie({'name': 'over18', 'value': '1'})
    driver.get('https://www.ptt.cc/bbs/Beauty/index.html')
    all_a = driver.find_elements(By.XPATH, '//div[@class="r-ent"]/div[@class="title"]/a')
    print(len(all_a))
    try:
        for a in all_a:
            [url, title] = [a.get_attribute('href'), a.text]
            print([url, title])

            if title.find('公告') >= 0:
                print('跳過')
                continue

            if title.find('大尺碼') >= 0:
                print('跳過')
                continue

            if title.find('肉特') >= 0:
                print('跳過')
                continue

            if title.find('帥哥') >= 0:
                print('跳過')
                continue

            if url in base.url:
                print('已存在')
                continue

            results = db.select(
                " SELECT id, name FROM fa_ptt WHERE `url` = '%s'" % (url))
            if len(results) < 1:
                base.url.append(url)
                media = []
                driver1 = base.defaultChrome()
                try:
                    print("-----")
                    print('Beauty : ' + title + ' / ' + url)
                    print("-----")
                    ouo_url = base.shotUrl(url)
                    base.sendTG(base.chat_id_image, '<a href="' + ouo_url + '">' + title + '</a>')
                    sql = "INSERT INTO `fa_ptt` (`name`, `url`, `title`, `createtime`, `updatetime`) VALUES ('%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))" % (
                    'Beauty', url, title)
                    if not base.isTest:
                        db.insert(sql)

                    driver1.get(url)
                    driver1.add_cookie({'name': 'over18', 'value': '1'})
                    driver1.get(url)
                    all_one_a = driver1.find_elements(By.XPATH, '//div[@id="main-content"]/a')
                    for one_a in all_one_a:
                        print(one_a.get_attribute('href'))
                        media.append(one_a.get_attribute('href'))
                except Exception as e:
                    print(e)
                driver1.close()
                driver1.quit()
                base.send_media_group(base.chat_id_image, media)
            else:
                print('已存在')
    except Exception as e:
        print(e)
    driver.close()
    driver.quit()

def Gamesale():
    ptt_screenshot('Gamesale','https://www.ptt.cc/bbs/Gamesale/index.html')

def Lifeismoney():
    ptt_screenshot('Lifeismoney','https://www.ptt.cc/bbs/Lifeismoney/index.html')

def forsale():
    ptt_screenshot('forsale','https://www.ptt.cc/bbs/forsale/index.html')

def ptt_screenshot(_title, _url):
    driver = base.defaultChrome()
    driver.get(_url)
    driver.add_cookie({'name': 'over18', 'value': '1'})
    driver.get(_url)
    all_a = driver.find_elements(By.XPATH, '//div[@class="r-ent"]/div[@class="title"]/a')
    print(len(all_a))
    try:
        for a in all_a:

            [url, title] = [a.get_attribute('href'), a.text]
            print([url, title])

            if a.text.find('公告') >= 0:
                print("跳過")
                continue
            if a.text.find('本文已被刪除') >= 0:
                print("跳過")
                continue

            if url in base.url:
                print('已存在')
                continue

            results = db.select(" SELECT id, name FROM fa_ptt WHERE `url` = '%s'" % (url))
            if len(results) < 1:

                base.url.append(url)

                sql = "INSERT INTO `fa_ptt` (`name`, `url`, `title`, `createtime`, `updatetime`) VALUES ('%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))" % (
                _title, url, title)
                if not base.isTest:
                    db.insert(sql)
                driver1 = base.defaultChrome()
                try:
                    driver1.get(url)
                    driver1.add_cookie({'name': 'over18', 'value': '1'})
                    driver1.get(url)
                    driver1.get_screenshot_as_file("python_ptt.png")
                    ouo_url = base.shotUrl(url)
                    with open("python_ptt.png", 'rb') as photo_file:
                        base.send_photo(base.chat_id_money, photo_file, '<a href="' + ouo_url + '">' + title + '</a>',
                                        True)
                except Exception as e:
                    print(e)
                driver1.close()
                driver1.quit()
            else:
                print('已存在')
    except Exception as e:
        base.sendTG(base.chat_id_test, str(e))
    driver.close()
    driver.quit()

# 以下關閉----------------------------------------------------------------------

def Nungvl():
    driver = base.defaultChrome()
    driver.get('https://nungvl.net/')
    all_a = driver.find_elements(By.XPATH, '//h2/a[@class="item-link"]')
    print(len(all_a))
    try:
        num_run = 0
        for a in all_a:

            [url, title] = [a.get_attribute('href'), a.text]
            print([url, title])

            results = db.select(
                " SELECT id, name FROM fa_ptt WHERE `url` = '%s'" % (url))
            if len(results) < 1 and num_run < 2:
                media = []
                driver1 = base.defaultChrome()
                try:
                    print("-----")
                    print('Nungvl : ' + title + ' / ' + url)
                    print("-----")
                    ouo_url = base.shotUrl(url)
                    base.sendTG(base.chat_id_image, '<a href="' + ouo_url + '">' + title + '</a>')
                    sql = "INSERT INTO `fa_ptt` (`name`, `url`, `title`, `createtime`, `updatetime`) VALUES ('%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))" % (
                    'Beauty', url, title)
                    if not base.isTest:
                        db.insert(sql)
                    num_run = num_run + 1
                    media = getNungvlPageImage(driver1, url, media)
                except Exception as e:
                    print(e)
                driver1.close()
                driver1.quit()
                base.send_media_group(base.chat_id_image, media)
            else:
                if num_run > 1:
                    print('兩次先略過')
                else:
                    print('已存在')
    except Exception as e:
        print(e)
    driver.close()
    driver.quit()

def getNungvlPageImage(driver1, url, media):
    driver1.get(url)
    print(url)
    base.time.sleep(1)
    all_img_a = driver1.find_elements(By.XPATH, '//div[@class="contentme"]/a/img')
    print(len(all_img_a))

    for one_img in all_img_a:
        print(one_img.get_attribute('src'))
        # base.send_photo(base.chat_id_image, one_img.get_attribute('src'))
        media.append(one_img.get_attribute('src'))

    try:
        a = driver1.find_element(By.XPATH, '//a[@class="pagination-link"][text()="Next >"]')
        [url_next] = [a.get_attribute('href')]
        media = getNungvlPageImage(driver1, url_next, media)
        return media
    except Exception as e:
        return media

def Playno1():
    driver = base.defaultChrome()
    driver.get('http://www.playno1.com/portal.php?mod=list&catid=78')
    a = driver.find_elements(By.XPATH, '//span[@class="ui-button-text"]/..')
    a[0].click()
    base.time.sleep(2)
    all_a = driver.find_elements(By.XPATH, '//div[@class="fire_float"]/ul/li/h3/a')
    print(len(all_a))
    try:
        for a in all_a:

            [url, title] = [a.get_attribute('href'), a.text]
            print([url, title])

            results = db.select(
                " SELECT id, name FROM fa_ptt WHERE `url` = '%s'" % (url))
            if len(results) < 1:
                media = []
                driver1 = base.defaultChrome()
                try:
                    print("-----")
                    print('Playno1 : ' + title + ' / ' + url)
                    print("-----")
                    ouo_url = base.shotUrl(url)
                    base.sendTG(base.chat_id_image, '<a href="' + ouo_url + '">' + title + '</a>')
                    sql = "INSERT INTO `fa_ptt` (`name`, `url`, `title`, `createtime`, `updatetime`) VALUES ('%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))" % (
                        'Beauty', url, title)

                    if not base.isTest:
                        db.insert(sql)

                    driver1.get(url)
                    print(url)
                    a = driver1.find_elements(By.XPATH, '//span[@class="ui-button-text"]/..')
                    a[0].click()
                    base.time.sleep(2)
                    all_img_a = driver1.find_elements(By.XPATH, '//img[@onload="thumbImg(this)"]')
                    print(len(all_img_a))

                    for one_img in all_img_a:
                        print(one_img.get_attribute('src'))
                        try:
                            one_img.get_attribute('src').index("back.gif")
                        except:
                            # base.send_photo(base.chat_id_image, one_img.get_attribute('src'))
                            media.append(one_img.get_attribute('src'))
                except Exception as e:
                    print(e)
                driver1.close()
                driver1.quit()
                base.send_media_group(base.chat_id_image, media)
            else:
                print('已存在')
    except Exception as e:
        print(e)
    driver.close()
    driver.quit()


def ClickMe():
    driver = base.defaultChrome()
    driver.get('https://clickme.net/c/beauty')
    all_a = driver.find_elements(By.XPATH, '//ul[@id="article-list"]/li/a')
    print(len(all_a))
    try:
        for a in all_a:
            [url, title] = [a.get_attribute('href'), a.text]
            print([url, title])

            results = db.select(
                " SELECT id, name FROM fa_ptt WHERE `url` = '%s'" % (url))

            if len(results) < 1:
                media = []
                driver1 = base.defaultChrome()
                try:
                    print("-----")
                    print('ClickMe : ' + title + ' / ' + url)
                    print("-----")
                    ouo_url = base.shotUrl(url)
                    base.sendTG(base.chat_id_image, '<a href="' + ouo_url + '">' + title + '</a>')
                    sql = "INSERT INTO `fa_ptt` (`name`, `url`, `title`, `createtime`, `updatetime`) VALUES ('%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))" % (
                        'ClickMe', url, title)
                    if not base.isTest:
                        db.insert(sql)
                    driver1.get(url)
                    try:
                        base.time.sleep(1)
                        el_close = driver.find_element(By.XPATH, '//div[@id="society-close"]')
                        el_close.click()
                        base.time.sleep(1)
                    except Exception as e:
                        print(e)
                    all_one_a = driver1.find_elements(By.XPATH, '//div[@id="primary"]/article/p/img')
                    print(len(all_one_a))
                    for one_a in all_one_a:
                        print(one_a.get_attribute('src'))
                        media.append(one_a.get_attribute('src'))
                except Exception as e:
                    print(e)
                driver1.close()
                driver1.quit()
                base.send_media_group(base.chat_id_image, media)
            else:
                print('已存在')
    except Exception as e:
        print(e)
    driver.close()
    driver.quit()

def ClickMe18():
    driver = base.defaultChrome()
    driver.get('https://r18.clickme.net/')
    try:
        time.sleep(3)
        el_close = driver.find_element(By.XPATH, '//button[@id = "enter"]')
        el_close.click()
        time.sleep(3)
        all_a = driver.find_elements(By.XPATH, '//ul[@id="newArticle"]/li/a')
        print(len(all_a))
        for a in all_a:
            [url, title] = [a.get_attribute('href'), a.text]
            print([url, title])

            results = db.select(
                " SELECT id, name FROM fa_ptt WHERE `url` = '%s'" % (url))

            if len(results) < 1:
                media = []
                driver1 = base.defaultChrome()
                try:
                    print("-----")
                    print('ClickMe : ' + title + ' / ' + url)
                    print("-----")
                    ouo_url = base.shotUrl(url)
                    base.sendTG(base.chat_id_image, '<a href="' + ouo_url + '">' + title + '</a>')
                    sql = "INSERT INTO `fa_ptt` (`name`, `url`, `title`, `createtime`, `updatetime`) VALUES ('%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))" % (
                        'ClickMe', url, title)
                    if not base.isTest:
                        db.insert(sql)
                    driver1.get(url)
                    try:
                        base.time.sleep(1)
                        el_close = driver.find_element(By.XPATH, '//div[@id="society-close"]')
                        el_close.click()
                        base.time.sleep(1)
                    except Exception as e:
                        print(e)
                    all_one_a = driver1.find_elements(By.XPATH, '//div[@id="primary"]/article/p/img')
                    print(len(all_one_a))
                    for one_a in all_one_a:
                        print(one_a.get_attribute('src'))
                        media.append(one_a.get_attribute('src'))
                except Exception as e:
                    print(e)
                driver1.close()
                driver1.quit()
                base.send_media_group(base.chat_id_image, media)
            else:
                print('已存在')
    except Exception as e:
        print(e)
    driver.close()
    driver.quit()