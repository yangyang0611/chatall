import mariadb
import sys
from internal import settings as setting
from internal.logger import create_logger

logger = create_logger("MariaDB Connector")
pool = None

def db_connect(user, passwd, host, port, dbname):
    logger.info("Establish single connection")
    try:
        conn = mariadb.connect(
            user=user,
            password=passwd,
            host=host,
            port=port,
            database=dbname,
        )
    except mariadb.Error as e:
        logger.error("Error connecting to MariaDB Platform: ", str(e))
        #print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    return conn

def create_connection_pool():
    global pool
    logger.info("Establish connection pool")
        
    try:
        cpool = mariadb.ConnectionPool(
            user=setting.get_settings().DB_USER, 
            password=setting.get_settings().DB_PASSWD, 
            host=setting.get_settings().DB_HOST, 
            port=setting.get_settings().DB_PORT, 
            database=setting.get_settings().DB_NAME,
            pool_name="web-app",
            pool_size=64
        )
        pool = cpool
        #return pool
        
    except mariadb.Error as e:
        logger.error("Error connecting to MariaDB Platform:", str(e))
        sys.exit(1)
        
def get_conn():
    global pool
    conn = pool.get_connection()
    return conn

def release_connection_pool():
    global pool
    status = 0
    try:
        pool.close()
    except Exception as e:
        print(str(e))
        status = -1
        return status
    finally:
        logger.info("Release pool with status " + str(status))
    return status

def init(conn):
    logger.info("Initialize tables")
    cur = conn.cursor()
    # CREATE TABLE USERS(UserId int PRIMARY KEY, UserName varchar(20), UserPassword varchar(20), Level int);
    sql = "CREATE TABLE if not exists USERS(UserId int AUTO_INCREMENT, UserName varchar(20), UserPassword varchar(20), Level int, Room int, Register int DEFAULT '0', PRIMARY KEY(UserId))" 
    cur.execute(sql)
    
    # CREATE TABLE ROOMS(RoomId int PRIMARY KEY, RoomName varchar(50));
    sql = "CREATE TABLE if not exists ROOMS(RoomId int AUTO_INCREMENT, RoomName varchar(50), RoomDescript varchar(100), UserLimit int, PRIMARY KEY(RoomId))"
    cur.execute(sql)
    
    # CREATE TABLE ROOM_<Id>(UserId int, Permission int, FOREIGN KEY(UserId) REFERENCES USERS(UserId) ON DELETE CASCADE);

    # create table for v2 user profile
    sql = "CREATE TABLE if not exists user_profiles(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), password VARCHAR(255), email VARCHAR(255), profile_picture VARCHAR(255), caption VARCHAR(255), friend_code VARCHAR(255), country VARCHAR(255), num_photos_uploaded INT)"
    cur.execute(sql)
    
    
    # create table for v2 user image
    sql = "CREATE TABLE if not exists user_img(UserId INT NOT NULL, ImgId VARCHAR(255) NOT NULL, Img LONGBLOB NOT NULL)"
    cur.execute(sql)
    cur.close()

def addUser(conn, username, userpassword) -> tuple[str, int]:
    logger.info("Add user to tables")
    user_id = None
    cur = conn.cursor()
    # default set user level to 0
    sql = "INSERT INTO USERS (`UserName`, `UserPassword`, `Level`, `Room`, `Register`) VALUES (%s, %s, 0, 0, 0)"
    logger.debug("addUser sql: " + sql)
    try:
        cur.execute(sql, (username, userpassword))
        user_id = int(cur.lastrowid)
    except Exception as e:
        logger.error(str(e))
    finally:
        conn.commit()
        cur.close()

    return "OK", user_id


def verifyUser(conn, username, userpassword) -> bool:
    logger.info("Verify user registration status")
    cur = conn.cursor()
    sql = "SELECT * FROM USERS WHERE username='" + username + "'"
    logger.debug("sql: " + sql)
    cur.execute(sql)
    result = cur.fetchone()
    if result is not None:
        stored_password = result[2]
        return stored_password == userpassword
    else:
        return False
    conn.commit()
    cur.close()

def getUserWithId(conn, userId) -> tuple[str, int, int, int]:
    logger.info("Get user info with user_id")
    cur = conn.cursor()
    sql = "SELECT UserName, Level, Room, UserId FROM USERS WHERE userId=%d"
    data = (userId, )
    logger.debug("sql: " + sql)
    cur.execute(sql, data)
    for UserName, Level, Room, UserId in cur:
        return UserName, Level, Room, UserId
    cur.close()
    
def getUserName(conn, userName) -> tuple[str, int]:
    logger.info("Get user level with user_name")
    cur = conn.cursor()
    sql = "SELECT Level FROM USERS WHERE userName=%s"
    data = (userName, )
    logger.debug("sql: " + sql)
    cur.execute(sql, data)
    for Level in cur:
        return userName, Level[0]
    cur.close()

def getUserWithName(conn, userName, userId) -> tuple[str, int]:
    logger.info("Get user level with user_name and user_id")
    cur = conn.cursor()
    sql = "SELECT Level FROM USERS WHERE userId=%d AND userName=%s"
    data = (userId, userName, )
    logger.debug("sql: " + sql)
    cur.execute(sql, data)
    for Level in cur:
        return userName, Level[0]
    cur.close()
    
def deleteUser(conn, userId) -> str:
    logger.info("Delete user with user_id")
    cur = conn.cursor()
    sql = "DELETE FROM USERS WHERE UserId=" + str(userId)
    cur.execute(sql)
    logger.debug("sql: " + sql)
    conn.commit()
    cur.close()
    
    return "OK"

def deleteUserWithName(conn, userId, userName) -> str:
    logger.info("Delete user with user_name")
    cur = conn.cursor()
    sql = "DELETE FROM USERS WHERE UserId=" + str(userId) + " AND UserName='" + userName + "'"
    logger.debug("sql: " + sql)
    cur.execute(sql)
    cur.close()
    conn.commit()
    
    return "OK"


def createRoom(conn, roomName, userLimit, userId, roomDescript) -> tuple[str, int]:
    logger.info("Create new room")
    room_id = None
    cur = conn.cursor()
    logger.info("Update room table")
    # Update Rooms table
    try:
        sql = "INSERT INTO ROOMS (RoomName, RoomDescript, UserLimit) VALUES('" + roomName + "', '" + roomDescript + "', " + str(userLimit) + ")"
        logger.debug("sql: " + sql)
        cur.execute(sql)
        room_id = int(cur.lastrowid)
        logger.debug("New room: " + str(room_id))
    except Exception as e:
        logger.error(str(e))
    finally:
        conn.commit()
    
    # Create room table to keep room status
    logger.info("Create new tables for room " + str(room_id))
    try:
        sql = "CREATE TABLE ROOM_" + str(room_id) + " (UserId int, Permission int, FOREIGN KEY(UserId) REFERENCES USERS(UserId) ON DELETE CASCADE)"
        logger.debug("sql: " + sql)
        cur.execute(sql)
    except Exception as e:
        logger.error(str(e))
    finally:
        conn.commit()
    
    # Insert user into room
    # Set user permission to 1 (admin)
    status = insertUserToRoom(conn, room_id, userId, 1)
    cur.close()
    if status != "OK":
        return "FAIL", -1
    
    return "OK", room_id

def insertUserToRoom(conn, roomId, userId, permis) -> str:
    logger.info("Insert user to room")
    logger.debug("Room id: " + str(roomId))
    logger.debug("User id: " + str(userId))
    cur = conn.cursor()
    try:
        sql = "INSERT INTO ROOM_" + str(roomId) + " VALUES(" + str(userId) + "," + str(permis) + ")"
        logger.debug("sql: " + sql)
        cur.execute(sql)
    except Exception as e:
        logger.error(str(e))
        return(str(e))
    finally:
        conn.commit()
            
    return "OK"

def updateUserRegStatus(conn, userId) -> str:
    logger.info("Update user registration statue to True")
    cur = conn.cursor()
    sql = "UPDATE USERS SET Register=1 WHERE UserId = " + str(userId);
    logger.debug("sql: " + sql)
    try:
        cur.execute(sql)
        conn.commit()
        return "SUCCESS"
    except Exception as e:
        logger.error(str(e))
        return "FAIL"
    finally:
        conn.commit()
        cur.close()

#TODO: Get how many people in room
#def getRoomLen(conn, roomName):

#TODO: clean up all table
#def clean(conn):

def create_user_profile(conn, user_profile) -> tuple[int, str]:
    logger.info("Create user profile")
    user_id = None
    cursor = conn.cursor()

    # Insert the user profile data into the database
    query = "INSERT INTO user_profiles (name, password, email, profile_picture, caption, friend_code, country, num_photos_uploaded) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    params = (
        user_profile.name,
        user_profile.password,
        user_profile.email,
        user_profile.profile_picture,
        user_profile.caption,
        user_profile.friend_code,
        user_profile.country,
        user_profile.num_photos_uploaded
    )
    logger.debug(query)
    try:
        cursor.execute(query, params)
    except Exception as e:
        logger.error(str(e))
        return -1, str(e)
    finally:
        user_id = cursor.lastrowid
        conn.commit()
        
        # Close the database connection
        cursor.close()
        conn.close()
    return 0, user_id
        
def create_user_picture(conn, user_picture) -> tuple[int, str]:
    logger.info("Create user picture")
    cursor = conn.cursor()
    query = "INSERT INTO your_table_name (UserId, ImgId, Img) VALUES (?, ?, ?)"
    params = (user_picture.user_id,  user_picture.url, user_picture.picture)
    logger.debug(query)
    
    try:
        cursor.execute(query, params)
    except Exception as e:
        logger.error(str(e))
        return -1, str(e)
    finally:
        conn.commit()
        conn.close()

    return 0, ""

def get_user_profile_field(conn, user_id, field) -> tuple[int, int]:
    cur = conn.cursor()
    sql = "SELECT " + field + " FROM user_profiles WHERE id=%d"
    data = (user_id,)
    logger.debug("sql: " + sql)
    cur.execute(sql, data)
    for field in cur:
        return 0, field[0]
    conn.commit()
    cur.close()
    
    return -1, 0

def update_user_photos_num(conn, user_id, offset) -> tuple[int, str]:
    logger.info("Update user images num")
    status, current_num = get_user_profile_field(conn, user_id=user_id, field="num_photos_uploaded")
    if status != 0:
        logger.error("Failed to get current user images num")
    
    num = current_num + offset
    logger.debug("Update num: " + str(num) + " = " + str(current_num) + " + " + str(offset))
    
    cur = conn.cursor()
    sql = "UPDATE user_profiles SET num_photos_uploaded=" + str(num) + " WHERE id = " + str(user_id)
    logger.debug("sql: " + sql)
    cur.execute(sql)
    cur.close()
    conn.commit()
    return 0, ""

def get_user_profile(conn, user_id) -> tuple[str, str, str, str, str, str, int]:
    logger.info("Get user profile with user_id")
    cur = conn.cursor()
    sql = "SELECT name, email, profile_picture, caption, friend_code, country, num_photos_uploaded FROM user_profiles WHERE id=%d"
    data = (user_id, )
    logger.debug("sql: " + sql)
    cur.execute(sql, data)
    for name, email, profile_picture, caption, friend_code, country, num_photos_uploaded in cur:
        return name, email, profile_picture, caption, friend_code, country, num_photos_uploaded
    cur.close()

def delete_user_profile(conn, user_id) -> tuple[int, str]:
    logger.info("Delete user profile with given user_id")
    
    cur = conn.cursor()
    sql = "DELETE FROM user_profiles WHERE id=" + str(user_id)
    logger.debug("sql: " + sql)
    try:
        cur.execute(sql)
    except Exception as e:
        logger.error(str(e))
        return "FAIL", str(e)
    finally:
        cur.close()
        conn.commit()
    
    return "OK", ""

def get_user_publice_info(conn, code) -> tuple[str, str]:
    logger.info("Get user profile with user_id")
    cur = conn.cursor()
    sql = "SELECT name, country FROM user_profiles WHERE friend_code='" + code + "'"
    logger.debug("sql: " + sql)

    cur.execute(sql)
    result = cur.fetchone()
    logger.debug(result[0] + " " + result[1])
    cur.close()
    
    return result[0], result[1]