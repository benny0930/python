
from selenium.webdriver.common.by import By

# base = db = None


def start(_base, _db):
    global base, db
    try:
        base = _base
        db = _db
        sql = "SELECT id, name , url , website, new_episode FROM fa_av_actor WHERE `active` LIKE 'Y' limit 1"  # test
        sql = "SELECT id, name , url , website, new_episode FROM fa_comic WHERE `active` LIKE 'Y'"
        results = db.select(sql)
        for row in results:
            print("-----------")
            print(row)
            [id, name, url, website, new_episode] = row
            if website == 'baozimh':
                baozimh(id, name, url, new_episode)
            elif website == 'cocomanga':
                cocomanga(id, name, url, new_episode)
    except Exception as e:
        base.sendTG(str(e))


def baozimh(id, name, url, new_episode):
    driver = base.defaultChrome()
    driver.get(url)
    base.reciprocal(1)
    last_episode = driver.find_element(
        By.XPATH, '//div[@class="supporting-text mt-2"]/div[2]/span/a').text
    # print('id : ' + str(id))
    print('name : ' + name + ' / last_episode : ' + last_episode + ' / new_episode : ' + new_episode)
    if last_episode != new_episode:
        base.sendTG('漫畫更新:'+name+"-"+last_episode)
        db.insert(" UPDATE `fa_comic` SET `new_episode`='%s', updatetime= UNIX_TIMESTAMP(NOW()), new='Y' WHERE  `id`='%s' "
                  % (last_episode, str(id)))

    print()
    driver.close()


def cocomanga(id, name, url, new_episode):
    driver = base.defaultChrome()
    driver.get(url)
    base.reciprocal(1)
    last_episode = driver.find_element(
        By.XPATH, '//dd[@class="fed-deta-content fed-col-xs7 fed-col-sm8 fed-col-md10"]/ul/li[5]/a').text
    # print('id : ' + str(id))
    print('name : ' + name + ' / last_episode : ' +
          last_episode + ' / new_episode : ' + new_episode)
    if last_episode != new_episode:
        base.sendTG('漫畫更新:'+name+"-"+last_episode)
        db.insert(" UPDATE `fa_comic` SET `new_episode`='%s', updatetime= UNIX_TIMESTAMP(NOW()), new='Y' WHERE  `id`='%s' "
                  % (last_episode, str(id)))

    print()
    driver.close()
