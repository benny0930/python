
from selenium.webdriver.common.by import By

# base = db = None


def start(_base, _db):
    global base, db
    try:
        base = _base
        db = _db
        sql = "SELECT id, name , url , website, new_episode FROM fa_av_actor WHERE `active` LIKE 'Y' limit 1"  # test
        sql = "SELECT id, name , url , website, new_episode FROM fa_comic WHERE `active` LIKE 'Y'"
        results = db.select(sql)
        for row in results:
            try:
                print("-----------")
                print(row)
                [id, name, url, website, new_episode] = row
                if website == 'baozimh':
                    baozimh(id, name, url, new_episode)
                if website == 'cocomanga':
                    cocomanga(id, name, url, new_episode)
            except Exception as e:
                base.sendTG(str(e))

        # baozimhKeep()

    except Exception as e:
        base.sendTG(str(e))




def baozimhKeep():
    driver = base.defaultChrome()
    driver.get('https://www.baozimh.com/user/my_bookshelf')
    if driver.find_element(By.XPATH, '//input[@id="stacked-email"]'):
        driver.find_element(By.XPATH, '//input[@id="stacked-email"]').send_keys('kevin01@mailnesia.com')
        driver.find_element(By.XPATH, '//input[@id="stacked-password"]').send_keys('qq112233')
        base.time.sleep(1)
        driver.find_element(By.XPATH, '//div[@type="submit"]').click()
        base.time.sleep(5)

    items = driver.find_elements(By.XPATH, '//div[@class="bookshelf-items"]')
    index = 1
    for item in items:
        try:
            print('------')
            title = driver.find_element(By.XPATH, '//div[@class="bookshelf-items"]['+str(index)+']/div[@class="info"]/ul/li/h4/a').text
            url = driver.find_element(By.XPATH, '//div[@class="bookshelf-items"]['+str(index)+']/div[@class="info"]/ul/li/h4/a').get_attribute('href')
            last_episode = driver.find_element(By.XPATH, '//div[@class="bookshelf-items"]['+str(index)+']/div[@class="info"]/ul/li[5]').text
            last_episode = last_episode.replace('最新章节: ', '')
            index = index + 1
            print([title,url,last_episode])

            results = db.select(" SELECT id, name, url, website, new_episode FROM fa_comic WHERE `url` = '%s'" % (url))
            if len(results) > 0 :
                [id, name, url, website, new_episode] = results[0]
                print([id, name, url, website, new_episode])
                if last_episode != new_episode:
                    base.sendTG('漫畫更新:'+name+"-"+last_episode)
                    db.insert(" UPDATE `fa_comic` SET `new_episode`='%s', updatetime= UNIX_TIMESTAMP(NOW()), createtime= UNIX_TIMESTAMP(NOW()), new='Y' WHERE  `id`='%s' "
                            % (last_episode, str(id)))
                else:
                    db.insert(" UPDATE `fa_comic` SET  createtime= UNIX_TIMESTAMP(NOW()) WHERE  `id`='%s' "
                            % (str(id)))
            else :
                base.sendTG('漫畫新增:'+name+"-"+last_episode)
                db.insert("INSERT INTO `fa_comic` (`name`, `url`, `new_episode`, `createtime`, `updatetime`, `new`) VALUES ('%s', '%s', '%s', UNIX_TIMESTAMP(NOW()) , UNIX_TIMESTAMP(NOW()), 'Y')"
                        % (title, url, last_episode))
        except Exception as e:
            base.sendTG(str(e))

    print()
    driver.close()

def baozimh(id, name, url, new_episode):
    driver = base.defaultChrome()
    driver.get(url)
    base.reciprocal(1)
    last_episode = driver.find_element(
        By.XPATH, '//div[@class="supporting-text mt-2"]/div[2]/span/a').text
    # print('id : ' + str(id))
    print('name : ' + name + ' / last_episode : ' + last_episode + ' / new_episode : ' + new_episode)
    if last_episode != new_episode:
        base.sendTG('漫畫更新:'+name+"-"+last_episode)
        db.insert(" UPDATE `fa_comic` SET `new_episode`='%s', updatetime= UNIX_TIMESTAMP(NOW()), createtime= UNIX_TIMESTAMP(NOW()), new='Y' WHERE  `id`='%s' "
                  % (last_episode, str(id)))
    else:
        db.insert(" UPDATE `fa_comic` SET  createtime= UNIX_TIMESTAMP(NOW()) WHERE  `id`='%s' "
                  % (str(id)))
    print()
    driver.close()


def cocomanga(id, name, url, new_episode):
    driver = base.defaultChrome()
    driver.get(url)
    base.reciprocal(1)
    last_episode = driver.find_element(
        By.XPATH, '//dd[@class="fed-deta-content fed-col-xs7 fed-col-sm8 fed-col-md10"]/ul/li[5]/a').text
    # print('id : ' + str(id))
    print('name : ' + name + ' / last_episode : ' +
          last_episode + ' / new_episode : ' + new_episode)
    if last_episode != new_episode:
        base.sendTG('漫畫更新:'+name+"-"+last_episode)
        db.insert(" UPDATE `fa_comic` SET `new_episode`='%s', updatetime= UNIX_TIMESTAMP(NOW()), new='Y' WHERE  `id`='%s' "
                  % (last_episode, str(id)))
    else:
        db.insert(" UPDATE `fa_comic` SET  createtime= UNIX_TIMESTAMP(NOW()) WHERE  `id`='%s' "
                  % (str(id)))
    print()
    driver.close()


    
