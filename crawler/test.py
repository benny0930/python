from selenium.webdriver.common.by import By
import base
media = []
driver1 = base.defaultChrome()
try:
    print("-----")

    url = 'https://clickme.net/57143'

    driver1.get(url)

    all_one_a = driver1.find_elements(By.XPATH, '//div[@id="primary"]/article/p/img')
    print(len(all_one_a))
    for one_a in all_one_a:
        print(one_a.get_attribute('src'))
        media.append(one_a.get_attribute('src'))
    print(media)


except Exception as e:
    print(e)
driver1.close()
driver1.quit()