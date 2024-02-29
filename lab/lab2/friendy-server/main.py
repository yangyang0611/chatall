from fastapi import FastAPI, APIRouter
from routers import users, rooms, sysadmin, users_v2
from internal import settings as setting
from fastapi.middleware.cors import CORSMiddleware
from internal import db
from internal.redis import config_redis
from internal.logger import create_logger, get_log_level
import logging
import os

logger = create_logger("main")
config_redis()
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://192.168.10.3:5001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

v1ApiRouter = APIRouter(
    prefix="/api/v1",
    responses={404: {"description": "Not found"}}
)

app.include_router(v1ApiRouter)
app.include_router(users.router)
app.include_router(rooms.router)
app.include_router(sysadmin.router)
app.include_router(users_v2.router)

if os.getenv('ENV') != "TEST":
    logger.info("In production/dev mode")
    db.create_connection_pool()
    conn = db.get_conn()
    db.init(conn)
    conn.close()

@app.get('/')
def get_root():
    logger.info("Following is current settings:")
    logger.info("DB HOST: " + setting.get_settings().DB_HOST)
    logger.info("DB NAME: " + setting.get_settings().DB_NAME)
    logger.info("DB PASSWD: " + setting.get_settings().DB_PASSWD)
    logger.info("DB PORT: " + str(setting.get_settings().DB_PORT))
    logger.info("Log level: " + get_log_level())
    return {"Status": "Ok"}
