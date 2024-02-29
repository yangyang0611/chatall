from fastapi import APIRouter, Request, HTTPException
from internal import db as DB
from internal import settings as setting
from models import rooms as room
from mariadb import PoolError
from internal.logger import create_logger

router = APIRouter(
    prefix="/api/v1"
)

logger = create_logger("router.room")

@router.post("/room", tags=["room"])
async def create_room(req: room.NewRoom) -> room.Room:
    status = None
    logger.info("Create room")
    room_dict = req.dict()
    logger.debug("Input data: " + str(room_dict))
    
    try:
        conn = DB.get_conn()
        status, id = DB.createRoom(conn, room_dict["roomName"], room_dict["limit"], room_dict["ownerId"], room_dict["descript"])
    except PoolError as pe:
        logger.warning("Connection pool run out of connection!")
        DB.release_connection_pool()
        DB.create_connection_pool()
        
        conn = DB.get_conn()
        status, id = DB.createRoom(conn, room_dict["roomName"], room_dict["limit"], room_dict["ownerId"], room_dict["descript"])
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
    
    if status != "OK":
        raise HTTPException(status_code=500, detail="Error occured, please check system logs for more information")
    return room.Room(id=id, name=room_dict["roomName"],limit=room_dict["limit"], descript=room_dict["descript"])
