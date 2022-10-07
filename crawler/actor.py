
from selenium.webdriver.common.by import By

base = db = None

def start(_base, _db):
    global base , db 
    try:
        base = _base
        db = _db
        sql = "SELECT name , url , website FROM fa_av_actor WHERE `active` LIKE 'Y' limit 1" # test 
        sql = "SELECT name , url , website FROM fa_av_actor WHERE `active` LIKE 'Y'"
        results = db.select(sql)
        for row in results:
            print("-----------")
            print(row)
            [name, url, website] = row
            missav(name, url)
    except Exception as e:
        print(e)
        base.sendTG(str(e))
    

def missav(name, url):
    driver = base.defaultChrome()
    driver.get(url)
    base.reciprocal(10)
    divList1 = driver.find_elements(
        By.XPATH, '//div[@class="thumbnail group"]/div[1]')
    divList2 = driver.find_elements(
        By.XPATH, '//div[@class="thumbnail group"]/div[2]')
    # print(len(divList))
    index = 0
    for div in divList1:
        aList = div.find_elements(By.XPATH, './/a')
        # print(len(aList))
        if len(aList) == 3:
            span = aList[1].find_element(By.XPATH, './/span')
            a = divList2[index].find_element(By.XPATH, './/a')
            av_type = span.get_attribute('innerHTML').strip()
            av_url = a.get_attribute('href').strip()
            av_name = a.get_attribute('innerHTML').strip()
            print("-----")
            print(av_type + ' / ' + av_url + ' / ' + av_name)
            db.insert("INSERT INTO `fa_av_work` (`actor`, `name`, `av_type`, `url`, `createtime`, `updatetime`) VALUES ('%s', '%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW())) ON DUPLICATE KEY UPDATE `updatetime`=UNIX_TIMESTAMP(NOW()) "
                      % (name, av_name, av_type, av_url))
        index += 1
    print()
    driver.close()
