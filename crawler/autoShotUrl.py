import threading
from selenium.webdriver.common.by import By

def start(_base, _db):
    global base, db
    try:
        base = _base
        db = _db
        t = threading.Thread(target=ouo, args=())
        t.start()  # 開始
    except Exception as e:
        pass
    return True

def ouo():
    results = db.select(" SELECT url FROM fa_ptt ORDER BY RAND() LIMIT 1")
    [url] = results[0]
    driver = base.defaultChrome()
    try:
        print("-----------")
        driver.get(base.shotUrl(url))
        # id="btn-main"
        driver.find_element(By.XPATH, '//button[@id="btn-main"]').click()
        base.time.sleep(5)
        driver.find_element(By.XPATH, '//button[@id="btn-main"]').click()
        base.time.sleep(5)
        driver.find_element(By.XPATH, '//button[@id="btn-main"]').click()
        base.time.sleep(5)
        driver.find_element(By.XPATH, '//button[@id="btn-main"]').click()
    except Exception as e:
        if driver:
            driver.close()
