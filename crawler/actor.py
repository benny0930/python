import threading
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

base = db = None


def start(_base, _db):

    global base, db
    try:
        base = _base
        db = _db
        sql = "SELECT id, name , url , website FROM fa_av_actor WHERE `active` LIKE 'Y' limit 1"  # test
        sql = "SELECT id, name , url , website FROM fa_av_actor WHERE `active` LIKE 'Y'"
        results = db.select(sql)
        for row in results:
            try:
                print("-----------")
                print(row)
                [id, name, url, website] = row
                # missav(name, url)
                t = threading.Thread(target=missav, args=(id, name, url,))
                t.start()  # 開始
            except Exception as e:
                print(e)
                base.sendTG(base.chat_id_test, name + " : " + str(e))
            base.time.sleep(1)
    except Exception as e:
        print(e)
        base.sendTG(base.chat_id_test, str(e))

    return True


def missav(id, name, url):
    driver = base.defaultChrome()
    try:
        driver.set_page_load_timeout(5)
        try:
            driver.get(url)
            driver.find_elements(
                By.XPATH, '//div[@class="thumbnail group"]/div[1]')
        except TimeoutException:
            driver.execute_script(
                'window.stop ? window.stop() : document.execCommand("Stop");')
        driver.set_page_load_timeout(30)
        # base.reciprocal(1)
        divList1 = driver.find_elements(
            By.XPATH, '//div[@class="thumbnail group"]/div[1]')
        divList2 = driver.find_elements(
            By.XPATH, '//div[@class="thumbnail group"]/div[2]')
        # print(len(divList))
        # results = db.select(" SELECT group_concat(url) FROM fa_av_work WHERE 1 ")
        # av_url_list = []
        # if results[0][0]:
        #     av_url_list = results[0][0].split(',')
        # print(results)
        index = 0
        for div in divList1:
            aList = div.find_elements(By.XPATH, './/a')
            # if len(aList) == 3:
            span = aList[1].find_element(By.XPATH, './/span')
            a = divList2[index].find_element(By.XPATH, './/a')
            av_type = span.get_attribute('innerHTML').strip().replace("'",'')
            av_url = a.get_attribute('href').strip().replace("'",'').replace(":80",'')
            av_name = a.get_attribute('innerHTML').strip().replace("'",'')

            results = db.select(
                " SELECT id, name FROM fa_av_work WHERE `url` = '%s'" % (av_url))
            if len(results) > 0:
                print('已存在 : ' + av_type + ' / ' + av_url + ' / ' + av_name)
                db.insert(" UPDATE `fa_av_actor` SET updatetime= UNIX_TIMESTAMP(NOW()) WHERE  `id`='%s' "
                  % (str(id)))
            else:
                print("-----")
                print('影片更新 : ' + name + ' / ' + av_name + ' / ' + av_type + ' / ' + av_url)
                print("-----")
                base.sendTG(base.chat_id_test, '影片更新:'+name+"-"+av_name)
                sql = "INSERT INTO `fa_av_work` (`actor`, `name`, `av_type`, `url`, `createtime`, `updatetime`) VALUES ('%s', '%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))" % (name, av_name, av_type, av_url)
                db.insert(sql)
                

            # if av_url in av_url_list:
            #     print('已存在')
            # else:
            #     base.sendTG(base.chat_id_test, '影片更新:'+name+"-"+av_name)
            #     db.insert("INSERT INTO `fa_av_work` (`actor`, `name`, `av_type`, `url`, `createtime`, `updatetime`) VALUES ('%s', '%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))"
            #             % (name, av_name, av_type, av_url))

            index += 1
    except Exception as e:
        print(e)
        base.sendTG(base.chat_id_test, str(e))
    driver.close()
