import threading
from selenium.webdriver.common.by import By

# base = db = None


def set(_base, _db):
    global base, db
    base = _base
    db = _db


def start(_base, _db, index=0):
    set(_base, _db)
    try:
        # 看板 Gamesale
        title = 'Gamesale'
        results = db.select(" SELECT id, title, is_active, val FROM fa_is_open WHERE `title` = '%s'" % (title))
        [id, title, is_active, val] = results[0]
        if is_active == 'Y' and index % int(val) == 0:
            t = threading.Thread(target=Gamesale, args=())
            t.start()  # 開始

        # 看板 Beauty
        title = 'Beauty'
        results = db.select(" SELECT id, title, is_active, val FROM fa_is_open WHERE `title` = '%s'" % (title))
        [id, title, is_active, val] = results[0]
        if is_active == 'Y' and index % int(val) == 0:
            t = threading.Thread(target=Beauty, args=())
            t.start()  # 開始

        # https://nungvl.net/
        title = 'Nungvl'
        results = db.select(" SELECT id, title, is_active, val FROM fa_is_open WHERE `title` = '%s'" % (title))
        [id, title, is_active, val] = results[0]
        if is_active == 'Y' and index % int(val) == 0:
            # base.sendTG(base.chat_id_test, 'Nungvl Start')
            t = threading.Thread(target=Nungvl, args=())
            t.start()  # 開始


        # http://www.playno1.com/portal.php?mod=list&catid=78
        # title = 'Playno1'
        # results = db.select(" SELECT id, title, is_active, val FROM fa_is_open WHERE `title` = '%s'" % (title))
        # [id, title, is_active, val] = results[0]
        # if is_active == 'Y' and index % int(val) == 0:
        #     # base.sendTG(base.chat_id_test, 'Playno1 Start')
        #     t = threading.Thread(target=Playno1, args=())
        #     t.start()  # 開始
        

    except Exception as e:
        base.sendTG(base.chat_id_test, str(e))

    return True



def Gamesale():
    driver = base.defaultChrome()
    driver.get('https://www.ptt.cc/bbs/Gamesale/index.html')
    driver.add_cookie({'name': 'over18', 'value': '1'})
    driver.get('https://www.ptt.cc/bbs/Gamesale/index.html')

    all_a = driver.find_elements(By.XPATH, '//div[@class="r-ent"]/div[@class="title"]/a')
    print(len(all_a))

    try:
        for a in all_a:
            if a.text.find('公告') >= 0:
                break
            if a.text.find('NS') < 0:
                continue
            [url,title] = [a.get_attribute('href'), a.text]
            results = db.select(
                " SELECT id, name FROM fa_ptt WHERE `url` = '%s'" % (url))
            if len(results) < 1:
                sql = "INSERT INTO `fa_ptt` (`name`, `url`, `title`, `createtime`, `updatetime`) VALUES ('%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))" % ('Gamesale', url, title)
                if not base.isTest :
                    db.insert(sql)
                driver1 = base.defaultChrome()
                try:
                    driver1.get(url)
                    driver1.add_cookie({'name': 'over18', 'value': '1'})
                    driver1.get(url)
                    driver1.get_screenshot_as_file("python_ptt.png")
                    base.send_photo('-1001742966379', open("python_ptt.png", "rb"), '<pre>Gamesale : ' + title + ' </pre>' + url )

                except Exception as e:
                    print(e)
                driver1.close()


    except Exception as e:
            base.sendTG(base.chat_id_test, str(e))

    driver.close()

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

            results = db.select(
                    " SELECT id, name FROM fa_ptt WHERE `url` = '%s'" % (url))
            if len(results) < 1:
                driver1 = base.defaultChrome()
                try:
                    print("-----")
                    print('Beauty : ' + title + ' / ' + url)
                    print("-----")
                    base.sendTG(base.chat_id_image, '<pre>' + title + '</pre>' + url)
                    sql = "INSERT INTO `fa_ptt` (`name`, `url`, `title`, `createtime`, `updatetime`) VALUES ('%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))" % ('Beauty', url, title)
                    if not base.isTest :
                        db.insert(sql)
                    
                    driver1.get(url)
                    driver1.add_cookie({'name': 'over18', 'value': '1'})
                    driver1.get(url)
                    all_one_a = driver1.find_elements(By.XPATH, '//div[@id="main-content"]/a')

                    for one_a in all_one_a:
                        print(one_a.get_attribute('href'))
                        base.send_photo(base.chat_id_image, one_a.get_attribute('href'))

                    
                except Exception as e:
                    print(e)

                driver1.close()
            else:
                print('已存在')

    except Exception as e:
        print(e)

    driver.close()

def Nungvl():
    driver = base.defaultChrome()
    driver.get('https://nungvl.net/')

    all_a = driver.find_elements(By.XPATH, '//h2/a[@class="item-link"]')
    print(len(all_a))
    try:
        for a in all_a:

            [url, title] = [a.get_attribute('href'), a.text]
            print([url, title])
            
            results = db.select(
                    " SELECT id, name FROM fa_ptt WHERE `url` = '%s'" % (url))
            if len(results) < 1:
                driver1 = base.defaultChrome()
                try:
                    print("-----")
                    print('Nungvl : ' + title + ' / ' + url)
                    print("-----")
                    base.sendTG(base.chat_id_image, '<pre>' + title + '</pre>' + url)
                    sql = "INSERT INTO `fa_ptt` (`name`, `url`, `title`, `createtime`, `updatetime`) VALUES ('%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))" % ('Beauty', url, title)
                    if not base.isTest :
                        db.insert(sql)
                    getNungvlPageImage(driver1, url)    
                except Exception as e:
                    print(e)
                driver1.close()
            else:
                print('已存在')
    except Exception as e:
        print(e)

    driver.close()

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
                driver1 = base.defaultChrome()
                try:
                    print("-----")
                    print('Playno1 : ' + title + ' / ' + url)
                    print("-----")
                    base.sendTG(base.chat_id_image, '<pre>' + title + '</pre>' + url)
                    sql = "INSERT INTO `fa_ptt` (`name`, `url`, `title`, `createtime`, `updatetime`) VALUES ('%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))" % (
                    'Beauty', url, title)

                    if not base.isTest :
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
                            base.send_photo(base.chat_id_image, one_img.get_attribute('src'))
                except Exception as e:
                    print(e)
                driver1.close()
            else:
                print('已存在')
    except Exception as e:
        print(e)

    driver.close()

def getNungvlPageImage(driver1, url):
    driver1.get(url)
    print(url)
    base.time.sleep(1)
    all_img_a = driver1.find_elements(By.XPATH, '//div[@class="contentme"]/a/img')
    print(len(all_img_a))
    for one_img in all_img_a:
        print(one_img.get_attribute('src'))
        base.send_photo(base.chat_id_image, one_img.get_attribute('src'))
    try:
        a = driver1.find_element(By.XPATH, '//a[@class="pagination-link"][text()="Next >"]')
        [url_next] = [a.get_attribute('href')]
        getNungvlPageImage(driver1, url_next)
    except Exception as e:
        pass