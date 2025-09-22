import pymysql

# HOST = "192.168.56.56"
HOST = "100.108.32.17"
USER = 'root'
PASSWORD = 'root'
DATABASE = 'benny'


def select(sql):
    db = pymysql.connect(host=HOST, user=USER,
                         password=PASSWORD, database=DATABASE)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        print(sql)
        print("Error: unable to fetch data")
        results = []
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
        results = cursor.fetchall()
    except:
        print("Error: unable to fetch data")
        results = []
    db.close()
    return results
