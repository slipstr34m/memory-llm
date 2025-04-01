import redis
from app.config import REDIS_HOST, REDIS_PORT, REDIS_PASS

REDIS_POOL = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASS,
    db=0,
    decode_responses=False,
    socket_timeout=1,
    socket_connect_timeout=1
)

redis_client = redis.Redis(connection_pool=REDIS_POOL)