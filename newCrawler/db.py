import pymysql

# HOST = "192.168.56.56"
HOST = "100.108.32.17"
USER = 'root'
PASSWORD = 'root'
DATABASE = 'benny'


def get_connection():
    """統一建立資料庫連線"""
    return pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset='utf8mb4')


def select(sql, params=None):
    """執行 SELECT，回傳查詢結果"""
    try:
        with get_connection() as db:
            with db.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
    except Exception as e:
        print("SELECT Failed:", sql)
        print("Params:", params)
        print("Error:", e)
        return []


def execute(sql, params=None, return_last_id=False):
    """
    執行 INSERT/UPDATE/DELETE
    return_last_id: 若為 INSERT 可回傳最後插入ID
    """
    try:
        with get_connection() as db:
            with db.cursor() as cursor:
                cursor.execute(sql, params)
                db.commit()
                if return_last_id:
                    return cursor.lastrowid
                return cursor.rowcount  # 影響的行數
    except Exception as e:
        print("SQL Failed:", sql)
        print("Params:", params)
        print("Error:", e)
        if 'db' in locals():
            db.rollback()
        return None


def handle_delete(two_days_ago):
    print("刪除 createtime <", two_days_ago)

    sql_list = [
        "DELETE FROM fa_ptt_images WHERE createtime < %s",
        "DELETE FROM fa_ptt_main WHERE createtime < %s",
        "DELETE FROM fa_ptt WHERE createtime < %s",
    ]
    for sql in sql_list:
        results = execute(sql, (two_days_ago,))
        print(results)


def select_fa_ptt(href_value):
    sql = "SELECT id, name FROM fa_ptt WHERE `url` = %s"
    return select(sql, (href_value,))


def insert_fa_ptt(type_, url, title):
    sql = """
          INSERT INTO `fa_ptt` (`name`, `url`, `title`, `createtime`, `updatetime`)
          VALUES (%s, %s, %s, UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW())) \
          """
    return execute(sql, (type_, url, title), return_last_id=True)


def insert_fa_ptt_main(ptt_id, title, type_, img_url, is_follow):
    sql_main = """
               INSERT INTO `fa_ptt_main` (`ptt_id`, `title`, `type`, `cover`, `is_follow`, `createtime`, `updatetime`)
               VALUES (%s, %s, %s, %s, %s, UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW())) \
               """
    return execute(sql_main, (ptt_id, title, type_, img_url, is_follow), return_last_id=True)


def insert_fa_ptt_images(main_id, href_value):
    results = select("SELECT id FROM fa_ptt_images WHERE image = %s", (href_value,))
    if results:
        print(f'已存在({results})\n')
        return False

    sql_main = """
               INSERT INTO fa_ptt_images (main_id, image, createtime, updatetime)
               VALUES (%s, %s, UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW())) \
               """
    execute(sql_main, (main_id, href_value), return_last_id=True)
    return True
