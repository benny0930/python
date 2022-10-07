import random
import base
import db
import comic
import actor


# 更新演員及作品-------------------------------------------------------------------

isChrome = input("is show chrome:")
base.set(isChrome)

while True:
    base.sendTG('開始更新')
    actor.start(base, db)
    comic.start(base, db)
    base.reciprocal(60*60+random.randrange(5, 15))
