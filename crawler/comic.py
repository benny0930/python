import threading
from selenium.webdriver.common.by import By

# base = db = None


def start(_base, _db):
    global base, db
    try:
        base = _base
        db = _db
        base.sendTG(base.chat_id_test, 'baozimhKeep Start')
        sql = "SELECT id, name , url , website, new_episode FROM fa_av_actor WHERE `active` LIKE 'Y' limit 1"  # test
        sql = "SELECT id, name , url , website, new_episode FROM fa_comic WHERE `active` LIKE 'Y'"
        results = db.select(sql)

        t = threading.Thread(target=baozimhKeep, args=())
        t.start()  # 開始
        
        for row in results:
            try:
                print("-----------")
                print(row)
                [id, name, url, website, new_episode] = row
                if website == 'baozimh':
                    continue
                    # baozimh(id, name, url, new_episode)
                    # t = threading.Thread(target=baozimh, args=(id, name, url, new_episode,))
                    # t.start()  # 開始
                if website == 'cocomanga':
                    # cocomanga(id, name, url, new_episode)
                    t = threading.Thread(target=cocomanga, args=(
                        id, name, url, new_episode,))
                    t.start()  # 開始
                base.time.sleep(1)
            except Exception as e:
                base.sendTG(base.chat_id_test, name + " : " + str(e))

    except Exception as e:
        base.sendTG(base.chat_id_test, str(e))

    return True


def baozimhKeep():
    driver = base.defaultChrome()
    driver.get('https://www.baozimh.com/user/my_bookshelf')
    base.time.sleep(5)
    if driver.find_element(By.XPATH, '//input[@id="stacked-email"]'):
        driver.find_element(
            By.XPATH, '//input[@id="stacked-email"]').send_keys('kevin01@mailnesia.com')
        driver.find_element(
            By.XPATH, '//input[@id="stacked-password"]').send_keys('qq112233')
        base.time.sleep(1)
        driver.find_element(By.XPATH, '//div[@type="submit"]').click()
        base.time.sleep(5)

    pages = driver.find_elements(By.XPATH, '//ul[@class="pager"][1]/li')
    page_index = 1
    print(len(pages))
    for page in pages:
        print('頁面'+str(page_index))
        driver.find_element(
            By.XPATH, '//ul[@class="pager"][1]/li['+str(page_index)+']').click()
        if (page_index > 1):
            print('切換頁面'+str(page_index))
            base.time.sleep(4)
        base.time.sleep(1)
        page_index = page_index + 1
        items = driver.find_elements(
            By.XPATH, '//div[@class="bookshelf-items"]')
        index = 1
        for item in items:
            try:
                print('------')
                title = driver.find_element(
                    By.XPATH, '//div[@class="bookshelf-items"]['+str(index)+']/div[@class="info"]/ul/li/h4/a').text
                url = driver.find_element(By.XPATH, '//div[@class="bookshelf-items"]['+str(
                    index)+']/div[@class="info"]/ul/li/h4/a').get_attribute('href')
                last_episode = driver.find_element(
                    By.XPATH, '//div[@class="bookshelf-items"]['+str(index)+']/div[@class="info"]/ul/li[5]').text
                last_episode = last_episode.replace('最新章节: ', '')
                index = index + 1
                new_url = url.split("_")
                url = new_url[0]
                print([title, url, last_episode])

                results = db.select(
                    " SELECT id, name, url, website, new_episode FROM fa_comic WHERE `url` = '%s'" % (url))
                if len(results) > 0:
                    [id, name, url, website, new_episode] = results[0]
                    print([id, name, url, website, new_episode])
                    if last_episode != new_episode:
                        base.sendTG(base.chat_id_test, '漫畫更新:'+name+"-"+last_episode)
                        db.insert(" UPDATE `fa_comic` SET `new_episode`='%s', updatetime= UNIX_TIMESTAMP(NOW()), createtime= UNIX_TIMESTAMP(NOW()), new='Y' WHERE  `id`='%s' "
                                  % (last_episode, str(id)))
                    else:
                        db.insert(" UPDATE `fa_comic` SET  createtime= UNIX_TIMESTAMP(NOW()) WHERE  `id`='%s' "
                                  % (str(id)))
                else:
                    base.sendTG(base.chat_id_test, '漫畫新增:'+title+"-"+last_episode)
                    db.insert("INSERT INTO `fa_comic` (`name`, `url`, `new_episode`, `createtime`, `updatetime`, `new`) VALUES ('%s', '%s', '%s', UNIX_TIMESTAMP(NOW()) , UNIX_TIMESTAMP(NOW()), 'Y')"
                              % (title, url, last_episode))
            except Exception as e:
                if driver:
                    driver.close()
                base.sendTG(base.chat_id_test, str(e))

    print()
    driver.close()


def baozimh(id, name, url, new_episode):
    driver = base.defaultChrome()
    driver.get(url)
    # base.reciprocal(1)
    last_episode = driver.find_element(
        By.XPATH, '//div[@class="supporting-text mt-2"]/div[2]/span/a').text
    # print('id : ' + str(id))
    driver.close()
    print('name : ' + name + ' / last_episode : ' +
          last_episode + ' / new_episode : ' + new_episode)
    if last_episode != new_episode and last_episode != '':
        base.sendTG(base.chat_id_test, '漫畫更新:'+name+"-"+last_episode)
        db.insert(" UPDATE `fa_comic` SET `new_episode`='%s', updatetime= UNIX_TIMESTAMP(NOW()), createtime= UNIX_TIMESTAMP(NOW()), new='Y' WHERE  `id`='%s' "
                  % (last_episode, str(id)))
    else:
        db.insert(" UPDATE `fa_comic` SET  createtime= UNIX_TIMESTAMP(NOW()) WHERE  `id`='%s' "
                  % (str(id)))


def cocomanga(id, name, url, new_episode):
    driver = False
    try:
        try:
            driver = base.defaultChrome()
            driver.get(url)
            base.time.sleep(5)
            h1 = driver.find_element(By.XPATH, '//center/h1[1]').text
            print(h1)
            if(h1=='请用正常浏览器观看，如果觉得是个意外，请反馈'):
                driver.close()
                return
        except Exception as e:
            pass

        # base.reciprocal(1)
        last_episode = driver.find_element(
            By.XPATH, '//dd[@class="fed-deta-content fed-col-xs7 fed-col-sm8 fed-col-md10"]/ul/li[4]/a').text
        # print('id : ' + str(id))
        driver.close()
        print('name : ' + name + ' / last_episode : ' +
            last_episode + ' / new_episode : ' + new_episode)
        if last_episode != new_episode:
            base.sendTG(base.chat_id_test, '漫畫更新:'+name+"-"+last_episode)
            db.insert(" UPDATE `fa_comic` SET `new_episode`='%s', updatetime= UNIX_TIMESTAMP(NOW()), new='Y' WHERE  `id`='%s' "
                    % (last_episode, str(id)))
        else:
            db.insert(" UPDATE `fa_comic` SET  createtime= UNIX_TIMESTAMP(NOW()) WHERE  `id`='%s' "
                    % (str(id)))
    except Exception as e:
        base.sendTG(base.chat_id_test, str(e))
        if driver:
            driver.close()
