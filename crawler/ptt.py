import threading
from selenium.webdriver.common.by import By

# base = db = None


def start(_base, _db):
    global base, db
    try:
        base = _base
        db = _db

        # 看板 Gamesale
        title = 'Gamesale'
        results = db.select(" SELECT id, title, is_active FROM fa_is_open WHERE `title` = '%s'" % (title))
        [id, title, is_active] = results[0]
        if is_active == 'Y':
            t = threading.Thread(target=Gamesale, args=())
            t.start()  # 開始

        # 看板 Beauty
        title = 'Beauty'
        results = db.select(" SELECT id, title, is_active FROM fa_is_open WHERE `title` = '%s'" % (title))
        [id, title, is_active] = results[0]
        if is_active == 'Y':
            t = threading.Thread(target=Beauty, args=())
            t.start()  # 開始
        
        

    except Exception as e:
        base.sendTG('-758395812', str(e))

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
            base.sendTG('-758395812', str(e))

    driver.close()

def Beauty():
    driver = base.defaultChrome()
    driver.get('https://www.ptt.cc/bbs/Beauty/index.html')
    driver.add_cookie({'name': 'over18', 'value': '1'})
    driver.get('https://www.ptt.cc/bbs/Beauty/index.html')

    all_a = driver.find_elements(By.XPATH, '//div[@class="r-ent"]/div[@class="title"]/a')

    try:
        for a in all_a:
            if a.text.find('公告') >= 0:
                continue
            
            if a.text.find('大尺碼') >= 0:
                continue

            if a.text.find('肉特') >= 0:
                continue

            [url, title] = [a.get_attribute('href'), a.text]
            
            results = db.select(
                    " SELECT id, name FROM fa_ptt WHERE `url` = '%s'" % (url))
            if len(results) < 1:
                driver1 = base.defaultChrome()
                try:
                    print("-----")
                    print('Beauty : ' + title + ' / ' + url)
                    print("-----")
                    base.sendTG('-1001771451912', '<pre>' + title + '</pre>' + url)
                    sql = "INSERT INTO `fa_ptt` (`name`, `url`, `title`, `createtime`, `updatetime`) VALUES ('%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))" % ('Beauty', url, title)
                    db.insert(sql)
                    
                    driver1.get(url)
                    driver1.add_cookie({'name': 'over18', 'value': '1'})
                    driver1.get(url)
                    all_one_a = driver1.find_elements(By.XPATH, '//div[@id="main-content"]/a')

                    for one_a in all_one_a:
                        print(one_a.get_attribute('href'))
                        base.send_photo('-1001771451912', one_a.get_attribute('href'))

                    
                except Exception as e:
                    print(e)

                driver1.close()
            
    except Exception as e:
        print(e)

    driver.close()
