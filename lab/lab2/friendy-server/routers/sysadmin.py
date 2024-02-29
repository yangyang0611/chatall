from fastapi import APIRouter, Request
from internal import db as DB
from internal import settings as setting
from models import rooms as room
from internal.logger import create_logger
from mariadb import PoolError as pe

router = APIRouter(
    prefix="/api/v1"
)

logger = create_logger("admin")

@router.get("/sysadmin")
async def init_db():
    conn = None
    #conn = DB.connect(setting.get_settings().DB_USER, setting.get_settings().DB_PASSWD, setting.get_settings().DB_HOST, setting.get_settings().DB_PORT, setting.get_settings().DB_NAME)
    logger.info("Reset connection pool")
    try:
        conn = DB.get_conn()
    except pe:
        logger.warning("Connection pool is empty, recreate pool...")
        DB.release_connection_pool()
        DB.create_connection_pool()
        conn = DB.get_conn()
    #DB.init(conn)
    logger.info("Release pool...")
    DB.release_connection_pool()
    logger.info("Create pool...")
    DB.create_connection_pool()
    
    return {"Status": "Ok"}

#@router.delete("/sysadmin"):
    