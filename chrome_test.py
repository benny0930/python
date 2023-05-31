import crawler.base as base
import urllib3
urllib3.disable_warnings()

def defaultChrome(debuggerAddress=""):
    global chrome_version
    chromedriver.install(cwd=True)
    chrome_options = Options()
    chrome_options.add_argument(
        f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')
    chrome_options.add_argument('--disable-gpu')  # 關閉GPU 避免某些系統或是網頁出錯
    # 將要封鎖的權限加入選項中
    chrome_options.add_argument("--disable-notifications")  # 封鎖通知
    chrome_options.add_argument("--disable-popup-blocking")  # 封鎖彈出窗口


    if (os.path.exists('./' + chrome_version)):
        service = Service('./' + chrome_version + '/chromedriver')
    else:
        service = Service('./chromedriver')

    if (debuggerAddress != ""):
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:" + debuggerAddress)


    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    # driver.minimize_window()
    if (debuggerAddress == ""):
        driver.maximize_window()
    return driver

def deTest(debuggerAddress=""):
    driver.get('https://clickme.net/c/beauty')
    all_a = driver.find_elements(By.XPATH, '//ul[@id="article-list"]/li/a')
    print(len(all_a))
    try:
        for a in all_a:
            [url, title] = [a.get_attribute('href'), a.text]
            print([url, title])

            results = db.select(
                " SELECT id, name FROM fa_ptt WHERE `url` = '%s'" % (url))

            if len(results) < 1:
                media = []
                driver1 = base.defaultChrome()
                try:
                    print("-----")
                    print('ClickMe : ' + title + ' / ' + url)
                    print("-----")
                    ouo_url = base.shotUrl(url)
                    base.sendTG(base.chat_id_image, '<a href="' + ouo_url + '">' + title + '</a>')
                    sql = "INSERT INTO `fa_ptt` (`name`, `url`, `title`, `createtime`, `updatetime`) VALUES ('%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))" % (
                        'Beauty', url, title)
                    if not base.isTest:
                        db.insert(sql)

                    driver1.get(url)

                    all_one_a = driver1.find_elements(By.XPATH, '//div[@id="primary"]/img')
                    for one_a in all_one_a:
                        print(one_a.get_attribute('src'))
                        media.append(one_a.get_attribute('src'))
                except Exception as e:
                    print(e)
                driver1.close()
                driver1.quit()
                base.send_media_group(base.chat_id_image, media)
            else:
                print('已存在')
    except Exception as e:
        print(e)
    driver.close()
    driver.quit()
try:
    chrome_version = "113"
    # debuggerAddress = ""
    debuggerAddress = "64165"
    driver = defaultChrome(debuggerAddress)
    deTest(debuggerAddress)
except Exception as e:
    traceback.print_exc()



