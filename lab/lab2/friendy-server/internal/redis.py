import aioredis
import os
    
redis_url = None

def config_redis():
    global redis_url
    redis_url="redis://" + os.getenv("redis_ip", "192.168.10.5") + ":" + os.getenv("redis_port", "6379")
    
    
def get_conn():
    conn = aioredis.from_url(redis_url)
    
    return conn