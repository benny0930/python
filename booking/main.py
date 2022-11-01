import base
import gc
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.by import By


def get_next_month(number=1):
    # 获取后几个月
    month_date = datetime.now().date() + relativedelta(months=number)
    return month_date.strftime("%Y-%m-%d 08:00:00")


timeString = get_next_month()
struct_time = time.strptime(timeString, "%Y-%m-%d %H:%M:%S")  # 轉成時間元組
time_stamp = str(int(time.mktime(struct_time))) + "000"  # 轉成時間戳
old_time_stamp = time_stamp
sec = 61
driver = base.defaultChrome()
url = "https://www.chu-yu.com.tw/index.php#book"
driver.get(url)

try:
    print('開始')
        
    time.sleep(1)
    if driver.find_element(By.XPATH, '//div[@class="close"]').is_displayed():
        driver.find_element(By.XPATH, '//div[@class="close"]').click()
    
    print('是否第一頁')
    if driver.find_element(By.XPATH, '//input[@id="input"]'):
        print('輸入電話')
        driver.find_element(
            By.XPATH, '//input[@id="input"]').send_keys('0906801833')
        driver.find_element(By.XPATH, '//input[@id="start_btn"]').click()
        time.sleep(1)

    print('是否第二頁')
    if driver.find_element(By.XPATH, '//select[@id="area"]'):
        print('地點類型')
        driver.find_element(
            By.XPATH, '//select[@id="area"]/option[@value="3"]').click()
        driver.find_element(
            By.XPATH, '//select[@id="cuisine"]/option[@value="1"]').click()
        time.sleep(1)
        driver.find_element(
            By.XPATH, '//select[@id="shop_tag"]/option[@value="16"]').click()
        time.sleep(1)

    print('是否第三頁')
    if driver.find_element(By.XPATH, '//input[@id="booking_time"]'):
        print('時間人數開始')
        driver.execute_script(
            'document.querySelector("div.img-wrapper").scrollIntoView();')
        driver.find_element(
            By.XPATH, '//input[@id="booking_time"]').click()
        driver.execute_script('$("div.datepicker-days th.next").click();')
        driver.execute_script(
            '$("div.datepicker-days td.day[data-date=\''+time_stamp+'\']").click();')
        driver.find_element(
            By.XPATH, '//input[@id="booking_time"]').click()
        driver.find_element(
            By.XPATH, '//select[@id="section"]/option[@value="19:40"]').click()
        driver.find_element(
            By.XPATH, '//select[@id="people"]/option[@value="2"]').click()
        driver.find_element(By.XPATH, '//input[@id="check_btn"]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//input[@id="next_btn"]').click()
        time.sleep(1)
        msg = driver.find_element(By.XPATH, '//p[@id="alert_area"]').text
        print(msg)
        if (msg == "該時段訂位已滿，請重新查詢或選擇其他有空時段"):
            driver.find_element(By.XPATH, '//div[@class="close"]').click()
        else:
            print('訂位成功???')
            time.sleep(60*60)
        print('時間人數結束')
except Exception as e:
    print(e)


while True:
    try:
        if sec > 9:
            sec = 0
            print('開始')
            
            print('關閉彈窗')
            if driver.find_element(By.XPATH, '//div[@class="close"]').is_displayed():
                driver.find_element(By.XPATH, '//div[@class="close"]').click()

            print('更新')
            driver.execute_script('location.reload();')
            time.sleep(1)

            print('關閉彈窗')
            if driver.find_element(By.XPATH, '//div[@class="close"]').is_displayed():
                driver.find_element(By.XPATH, '//div[@class="close"]').click()

            driver.find_element(
                By.XPATH, '//input[@id="s_booking_time"]').click()

            driver.execute_script(
                '$("div.datepicker-days td.day[data-date=\''+time_stamp+'\']").click();')
            driver.find_element(
                By.XPATH, '//input[@id="s_booking_time"]').click()
            driver.find_element(
                By.XPATH, '//select[@id="s_section"]/option[@value="19:40"]').click()
            driver.find_element(
                By.XPATH, '//select[@id="s_people"]/option[@value="2"]').click()
            driver.find_element(By.XPATH, '//input[@id="search"]').click()
            time.sleep(1)
            msg = driver.find_element(By.XPATH, '//p[@id="alert_area"]').text
            print(msg)
            if (msg == "該時段訂位已滿，請重新查詢或選擇其他有空時段"):
                driver.find_element(By.XPATH, '//div[@class="close"]').click()
            else:
                print('訂位成功???')
                time.sleep(60*60)
            print('再次查詢結束')

                
        print('檢查時間')
        if driver.find_element(By.XPATH, '//div[@class="close"]').is_displayed():
            driver.find_element(By.XPATH, '//div[@class="close"]').click()
        timeString = get_next_month()
        struct_time = time.strptime(timeString, "%Y-%m-%d %H:%M:%S")  # 轉成時間元組
        time_stamp = str(int(time.mktime(struct_time))) + "000"  # 轉成時間戳
        if time_stamp != old_time_stamp :
            old_time_stamp = time_stamp
            print('跨日')
            sec = 61
        else:
            sec = sec + 1
            print('沒有跨日-'+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ' / 10 秒後更新 : ' + str(sec))
            
            time.sleep(1)

        # if driver != None:
            # driver.close()
    except Exception as e:
        print(e)
    gc.collect()
