import time
import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

HOST = "192.168.56.56"
USER='homestead'
PASSWORD='secret'
DATABASE='homestead'

def defaultChrome():
    chrome_options = Options() 
    # chrome_options.add_argument('--headless')  # 啟動Headless 無頭
    # chrome_options.add_argument('--disable-gpu') #關閉GPU 避免某些系統或是網頁出錯
    driver = webdriver.Chrome(executable_path='../chromedriver',chrome_options=chrome_options) #套用設定
    return driver

def db_select(sql):
    db = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        print ("Error: unable to fetch data")
        results = []
    db.close()
    return results


def db_insert(sql):
    db = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    except:
        print ("Error: unable to fetch data")
        db.rollback()
    db.close()
    return False





# -------------------------------------------------------------------

results = db_select("SELECT * FROM fa_av_actor WHERE `active` LIKE 'Y'")
for row in results:
    print(row)
    actor_id = row[0]
    name = row[1]
    url = row[2]
    web = row[3]
    print('開始：' + name)
    driver = defaultChrome()
    driver.minimize_window()
    driver.get(url)
    
    time.sleep(1)
    divList1 = driver.find_elements(By.XPATH, '//div[@class="thumbnail group"]/div[1]')
    divList2 = driver.find_elements(By.XPATH, '//div[@class="thumbnail group"]/div[2]')
    # print(len(divList))
    index = 0            # Python's indexing starts at zero
    for div in divList1:
        aList = div.find_elements(By.XPATH, './/a')
        print(len(aList))
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
            db_insert("INSERT INTO `fa_av_work` (`actor`, `name`, `av_type`, `url`, `createtime`, `updatetime`) VALUES ('%s', '%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW())) ON DUPLICATE KEY UPDATE `updatetime`=UNIX_TIMESTAMP(NOW()) " 
            % (name,av_name,av_type,av_url))
        index += 1
    driver.close()





    
