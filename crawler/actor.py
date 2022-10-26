import threading
from selenium.webdriver.common.by import By

base = db = None


def start(_base, _db):
    
    global base, db
    try:
        base = _base
        db = _db

        base.sendTG('actor start')

        sql = "SELECT name , url , website FROM fa_av_actor WHERE `active` LIKE 'Y' limit 1"  # test
        sql = "SELECT name , url , website FROM fa_av_actor WHERE `active` LIKE 'Y'"
        results = db.select(sql)
        for row in results:
            try:
                print("-----------")
                print(row)
                [name, url, website] = row
                # missav(name, url)
                t = threading.Thread(target=missav, args=(name, url,))
                t.start()  # 開始
            except Exception as e:
                print(e)
                base.sendTG(name + " : " + str(e))
            base.time.sleep(1)
    except Exception as e:
        print(e)
        base.sendTG(str(e))

    return True


def missav(name, url):
    driver = base.defaultChrome()
    try:
        driver.get(url)
        # base.reciprocal(1)
        divList1 = driver.find_elements(
            By.XPATH, '//div[@class="thumbnail group"]/div[1]')
        divList2 = driver.find_elements(
            By.XPATH, '//div[@class="thumbnail group"]/div[2]')
        # print(len(divList))
        results = db.select(" SELECT group_concat(url) FROM fa_av_work WHERE `actor` = '%s'" % (name))
        av_url_list = []
        if results[0][0]:
            av_url_list = results[0][0].split(',')
        index = 0
        for div in divList1:
            aList = div.find_elements(By.XPATH, './/a')
            if len(aList) == 3:
                span = aList[1].find_element(By.XPATH, './/span')
                a = divList2[index].find_element(By.XPATH, './/a')
                av_type = span.get_attribute('innerHTML').strip()
                av_url = a.get_attribute('href').strip()
                av_name = a.get_attribute('innerHTML').strip()
                print("-----")
                print(av_type + ' / ' + av_url + ' / ' + av_name)
                if av_url in av_url_list:
                    print('已存在')
                else:
                    base.sendTG('影片更新:'+name+"-"+av_name)
                    db.insert("INSERT INTO `fa_av_work` (`actor`, `name`, `av_type`, `url`, `createtime`, `updatetime`) VALUES ('%s', '%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))"
                            % (name, av_name, av_type, av_url))

            index += 1
    except Exception as e:
        print(e)
        base.sendTG(str(e))
    driver.close()
