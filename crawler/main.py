import base
import db
import comic
import actor

# 更新演員及作品-------------------------------------------------------------------

isChrome = input("is show chrome:")
base.set(isChrome)

while True:
    comic.start(base, db)
    actor.start(base, db)
    base.time(60*60)

