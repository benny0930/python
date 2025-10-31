import pymysql
import time

# HOST = "192.168.56.56"
HOST = "100.108.32.17"
USER = 'root'
PASSWORD = 'root'
DATABASE = 'benny'


def select(sql):
    db = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
    results = 0
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception as e:
        print("SQL Failed:", sql)
        print("Error:", e)
    db.close()
    return results


def insert(sql, params=None):
    try:
        db = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        cursor = db.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        db.commit()
        return cursor.lastrowid  # 回傳最後插入的自動遞增ID
    except Exception as e:
        print("SQL Failed:", sql)
        print("Params:", params)
        print("Error:", e)
        db.rollback()
        return None
    finally:
        db.close()


def delete(sql):
    db = pymysql.connect(host=HOST, user=USER,
                         password=PASSWORD, database=DATABASE)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        affected_rows = cursor.rowcount
        results = {"deleted": affected_rows}
    except Exception as e:
        db.rollback()  # 若出錯，回滾
        print(f"Error: {e}")
        results = {"error": str(e)}
    finally:
        db.close()
    return results


def handle_delete(two_days_ago):
    print("刪除 createtime < " + str(two_days_ago))
    sql = "DELETE FROM fa_ptt_images WHERE createtime < " + str(two_days_ago)
    results = delete(sql)
    print(results)
    sql = "DELETE FROM fa_ptt_main WHERE createtime < " + str(two_days_ago)
    results = delete(sql)
    print(results)
    sql = "DELETE FROM fa_ptt WHERE createtime < " + str(two_days_ago)
    results = delete(sql)
    print(results)


def select_fa_ptt(href_value):
    return select(" SELECT id, name FROM fa_ptt WHERE `url` = '" + href_value + "'")


def insert_fa_ptt(type, url, title):
    sql = "INSERT INTO `fa_ptt` (`name`, `url`, `title`, `createtime`, `updatetime`) VALUES "
    sql += "('%s', '%s', '%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))" % (type, url, title)
    return insert(sql)


def insert_fa_ptt_main(ptt_id, title, type, img_url, is_follow):
    sql_main = """
               INSERT INTO `fa_ptt_main` (`ptt_id`, `title`, `type`, `cover`, `is_follow`, `createtime`,
                                          `updatetime`)
               VALUES (%s, %s, %s, %s, %s, UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW())) \
               """
    return insert(sql_main, (ptt_id, title, type, img_url, is_follow))


def insert_fa_ptt_images(main_id, href_value):
    results = select("SELECT id FROM fa_ptt_images WHERE image = '" + href_value + "'")
    if len(results) > 0:
        print(f'已存在({results})\n')
        return False

    sql_main = """
               INSERT INTO fa_ptt_images (main_id, image, createtime, updatetime)
               VALUES (%s, %s, UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW())) \
               """
    insert(sql_main, (main_id, href_value))
    return True
