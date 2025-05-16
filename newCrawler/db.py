import pymysql

# HOST = "192.168.56.56"
HOST = "192.168.10.10"
USER = 'homestead'
PASSWORD = 'secret'
DATABASE = 'homestead'


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


def insert(sql):
    try:
        db = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return True
    except Exception as e:
        print("SQL Failed:", sql)
        print("Error:", e)
        db.rollback()
        return False
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
