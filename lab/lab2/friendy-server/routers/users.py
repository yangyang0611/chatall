from fastapi import APIRouter, Request, Header, HTTPException, File, UploadFile
from internal import db as DB
from internal import settings as setting
from models import users as user
from mariadb import PoolError
from internal.logger import create_logger

from typing import Optional

router = APIRouter(
    prefix="/api/v1"
)

logger = create_logger("router.user")

fake_secret_token = "testonly"

fake_user_table = {
    "1": {"username": "test", "password": "test", "level": 0, "room": 0}
}

@router.post("/file")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

@router.post("/user", tags=["user"])
async def create_user(req: user.NewUser, x_token: Optional[str] = Header(None)) -> user.User:
    user_dict = req.dict()
    if x_token == fake_secret_token:
        logger.info("Create user in test mode.")
        user_id = str(len(fake_user_table) + 1)
        if user_dict["password"] == "":
            raise HTTPException(status_code=400, detail="Password is null")
        fake_user_table[user_id] =  { "username": user_dict["username"], "password": user_dict["password"], "level": 0, "room": 0}
        return user.User(name=user_dict["username"], password=user_dict["password"], level=0, id=user_id, room=0)
    
    #conn = DB.connect(setting.get_settings().DB_USER, setting.get_settings().DB_PASSWD, setting.get_settings().DB_HOST, setting.get_settings().DB_PORT, setting.get_settings().DB_NAME)
    logger.info("Create user")
    try:
        conn = DB.get_conn()
        status, userId = DB.addUser(conn, user_dict["username"], user_dict["password"])
        logger.debug("User id: " + str(userId) + " status: " + status)
    except PoolError as pe:
        logger.warning("Connection pool run out of connection!")
        DB.release_connection_pool()
        DB.create_connection_pool()
        
        conn = DB.get_conn()
        status, userId = DB.addUser(conn, user_dict["username"], user_dict["password"])
        logger.debug("User id: " + str(userId) + " status: " + status)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
    
    return user.User(name=user_dict["username"], password=user_dict["password"], level=0, id=userId, room=0) 

@router.delete("/user/{user_id}", tags=["user"])
async def delete_user(user_id: int):
    logger.info("Delete user")
    
    try:
        conn = DB.get_conn()
        logger.debug("user_id: ", str(user_id))
        status = DB.deleteUser(conn, user_id)
    except PoolError as pe:
        logger.warning("Connection pool run out of connection!")
        DB.release_connection_pool()
        DB.create_connection_pool()
        
        conn = DB.get_conn()
        logger.debug("user_id: ", str(user_id))
        status = DB.deleteUser(conn, user_id)
    except Exception as e:
        logger.error(str(e))
    finally:
        conn.close()
    return {"Status": status}

@router.put("/user/{user_id}", tags=["user"])
async def update_user(user_id: int, req: user.UpdateUser, x_token: Optional[str] = Header(None)):
    conn = None
    user_dict = req.dict()
    if x_token == fake_secret_token:
        logger.info("Update user in test mode!")
        if (user_dict["room"] != None):
            try:
                fake_user_table[str(user_id)]
            except Exception:
                raise HTTPException(status_code=400, detail="User not exist")
            return {"Update User RoomId": user_dict["room"]}
    try:
        conn = DB.get_conn()
    except PoolError as pe:
        logger.warning("Connection pool run out of connection!")
        DB.release_connection_pool()
        DB.create_connection_pool()
        conn = DB.get_conn()
        
    if (user_dict["room"] != None):
        logger.info("Update user to room")
        logger.debug("Room: " + str(user_dict["room"]) + " User id: " + str(user_id))
        try:
            status = DB.insertUserToRoom(conn, user_dict["room"], user_id, user_dict["roomAdmin"])
            logger.debug("DB operation status: " + status)
        except Exception as e:
            logger.error(str(e))
        except PoolError as pe:
            logger.warning("Connection pool run out of connection!")
            DB.release_connection_pool()
            DB.create_connection_pool()
            status = DB.insertUserToRoom(conn, user_dict["room"], user_id, user_dict["roomAdmin"])
            logger.debug("DB operation status: " + status)
        finally:
            conn.close()
        #TODO: Update user status
        
        return {"Update User RoomId": user_dict["room"]}
    else:
        #TODO: Update user level
        return {"Pass"}

@router.get("/user/{user_id}", tags=["user"])
async def get_user(user_id: int, x_token: Optional[str] = Header(None)) -> user.User:
    if x_token == fake_secret_token:
        logger.info("Get user id in test mode!")
        try:
            data = fake_user_table[str(user_id)]
            return user.User(id=str(user_id), name=data["username"], password="*", level=data["level"], room=data["room"])
        except KeyError:
            raise HTTPException(status_code=400, detail="User not exist")
    #conn = DB.connect(setting.get_settings().DB_USER, setting.get_settings().DB_PASSWD, setting.get_settings().DB_HOST, setting.get_settings().DB_PORT, setting.get_settings().DB_NAME)
    logger.info("Get user")
    try:
        logger.debug("Get user with id: ", user_id)
        conn = DB.get_conn()
        userName, userLevel, userRoom, userId = DB.getUserWithId(conn, user_id)
        logger.debug(" user name: " + userName + " user level: " + userLevel + " user room: " + userRoom + " user id: " + userId)
    except PoolError as pe:
        logger.warning("Connection pool run out of connection!")
        DB.release_connection_pool()
        DB.create_connection_pool()
        logger.debug("Get user with id: ", user_id)
        conn = DB.get_conn()
        userName, userLevel, userRoom, userId = DB.getUserWithId(conn, user_id)
        logger.debug("user name: ", userName, "user level: ", userLevel, "user room: ", userRoom, "user id: ", userId)
    except Exception:
        logger.error("User may not exist")
        raise HTTPException(status_code=400, detail="User not exist")
    finally:
        conn.close()
    return user.User(id=userId, name=userName, password="*", level=userLevel, room=userRoom)
    
@router.put("/management/login/{user_id}", status_code=204, tags=["user"])
async def update_user_registration_state(user_id: int):
    logger.info("Update user registration state")
    
    try:
        conn = DB.get_conn()
        logger.debug("user id: " + str(user_id))
        status = DB.updateUserRegStatus(conn, user_id)
        if status != "SUCCESS":
            HTTPException(status_code=500, detail="Failed to update user status")
    except PoolError as pe:
        logger.warning("Connection pool run out of connection!")
        DB.release_connection_pool()
        DB.create_connection_pool()
        conn = DB.get_conn()
        logger.debug("user id: " + str(user_id))
        status = DB.updateUserRegStatus(conn, user_id)
        if status != "SUCCESS":
            HTTPException(status_code=500, detail="Failed to update user status")
    except Exception as e:
        logger.error(str(e))
    finally:
        conn.close()