import sys
sys.path.append('..')

from internal import db as DB
from internal import settings as setting 

def main():
    #conn = DB.dbConnect()
    conn = DB.db_connect(setting.get_settings().DB_USER, setting.get_settings().DB_PASSWD, setting.get_settings().DB_HOST, setting.get_settings().DB_PORT, "mysql")
    print("Connect to Host: " + setting.get_settings().DB_HOST)
    cur = conn.cursor()
    sql = "DROP DATABASE " + setting.get_settings().DB_NAME
    cur.execute(sql)
    conn.commit()
    print("Drop DB: " + setting.get_settings().DB_NAME)
    
    sql = "CREATE DATABASE " + setting.get_settings().DB_NAME
    cur.execute(sql)
    conn.commit()
    print("Create DB: " + setting.get_settings().DB_NAME)

if __name__ == '__main__':
    main()
