import base
import db
import time
from selenium.webdriver.common.by import By


def missav(name, url):
    driver = base.defaultChrome()
    driver.get(url)
    time.sleep(1)
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
            print(av_type)
            print(av_url)
            print(av_name)
            print("-----")
            print("")
            db.insert("INSERT INTO `fa_av_work` (`actor`, `name`, `av_type`, `url`, `createtime`, `updatetime`) VALUES ('%s', '%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW())) ON DUPLICATE KEY UPDATE `updatetime`=UNIX_TIMESTAMP(NOW()) "
                      % (name, av_name, av_type, av_url))
        index += 1
    driver.close()


# 更新演員及作品-------------------------------------------------------------------
# results = db.select("SELECT name , url , website FROM fa_av_actor WHERE `active` LIKE 'Y' limit 1") # test
results = db.select(
    "SELECT name , url , website FROM fa_av_actor WHERE `active` LIKE 'Y'")
for row in results:
    print(row)
    [name, url, website] = row
    missav(name, url)
