from redis import Redis

from ai_platform.config import settings


def is_redis_ok():
    try:
        r = Redis.from_url(settings.REDIS_URL, socket_connect_timeout=1)  # short timeout for the test
        response = r.ping()
    except Exception as e:
        return False
    return response


async def is_mongo_ok(mongodb_client):
    try:
        mongo_result = await mongodb_client.server_info()
        mongo_status = mongo_result.get("ok") == 1
    except Exception:
        mongo_status = False
    return mongo_status