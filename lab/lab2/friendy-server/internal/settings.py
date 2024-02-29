import os

from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = 13306
    DB_USER: str = 'root'
    DB_PASSWD: str = 'password'
    DB_NAME: str = 'FRIENDY'

class Development(Settings):
    DB_HOST = "192.168.0.117"
    
class Production(Settings):
    DB_HOST = "mariadb.default.svc"

class Test(Settings):
    DB_HOST = "mariadb.dev.svc"

def get_settings():
    env = os.getenv('ENV', 'LOCALDEV')
    if env == "PRODUCTION":
        return Production()
    if env == "TEST":
        return Test()
    return Development()
        
settings = get_settings()
