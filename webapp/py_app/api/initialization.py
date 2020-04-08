from api.handlers import HttpHandlers
import redis


def init_http_handlers(redis_host: str, redis_port: int, redis_pass: str) -> None:
    "creates a redis client on the HttpHandlers"
    if not len(redis_host) or (redis_port <= 0 or redis_port > 65535) or not len(redis_pass):
        raise ValueError("Invalid Redis Details")

    try:
        HttpHandlers.redis_client = redis.Redis(host=redis_host, port=redis_port, password=redis_pass, db=0)
    except Exception as ex:
        raise ConnectionError(str(ex))
