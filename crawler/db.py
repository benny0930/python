import pymysql

# HOST = "192.168.56.56"
HOST = "35.236.147.170"
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
        print("Error: unable to fetch data")
        results = []
    db.close()
    return results


def insert(sql):
    db = pymysql.connect(host=HOST, user=USER,
                         password=PASSWORD, database=DATABASE)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    except:
        print("Error: unable to fetch data")
        db.rollback()
    db.close()
    return False
