import random
import base
import db
import gc


# 更新演員及作品-------------------------------------------------------------------

isChrome = "N"
isLoop = True

while isLoop:
    isLoop = False
    base.sendTG('開始更新')
    try:
        import comic
        import actor
        actor.start(base, db)
        comic.start(base, db)
        del actor , comic
    except Exception as e:
        print(e)
        base.sendTG(str(e))
    # base.reciprocal(60*6+random.randrange(1, 6))
    gc.collect()

