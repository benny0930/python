
from selenium.webdriver.common.by import By
import base

base.set('Y')
url = "https://www.cocomanga.com/manga-cd68138/"

driver = base.defaultChrome()
driver.get(url)
# base.reciprocal(1)
last_episode = driver.find_element(
    By.XPATH, '//dd[@class="fed-deta-content fed-col-xs7 fed-col-sm8 fed-col-md10"]/ul/li[5]/a').text

print(last_episode)