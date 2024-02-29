import mariadb
import sys

def connect(user, passwd, host, port, dbname):
    try:
        conn = mariadb.connect(
            user="root",
            password="demo",
            host="192.168.1.184",
            port=3306,
            database="app"
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def init(conn):
    cur = conn.cursor()
    sql = "CREATE TABLE WEB (api varchar(50), counter int)" 
    cur.execute(sql)
    conn.commit()

def addCount(conn, url):
    cur = conn.cursor()
    try:
        count = getCount(conn, url)
        count += 1
        sql = "UPDATE WEB SET counter = %d WHERE api = %s;"
        cur.execute(sql, (count, url))
        conn.commit()
    except TypeError as e:
        sql = "INSERT INTO WEB (api, counter) VALUES (?, ?)"
        val = (url, 2)
        cur.execute(sql, val)
        conn.commit()

def getTables(conn):
    cur = conn.cursor()
    sql = "SELECT api, counter FROM WEB;"
    cur.execute(sql)
    records = cur.fetchall()

    conn.commit()
    for (api, counter) in records:
        return api, counter, cur.rowcount

def getCount(conn, url):
    cur = conn.cursor()
    sql = "SELECT counter FROM WEB WHERE api=?"
    val = (url,)
    cur.execute(sql, val)
    conn.commit()
    for counter in cur:
        return counter[0]
