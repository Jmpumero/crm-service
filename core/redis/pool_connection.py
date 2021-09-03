import aioredis

from config import config

global_settings = config.Settings()


async def init_redis_pool() -> aioredis.Redis:

    if global_settings.redis_password:
        redis = await aioredis.from_url(
            global_settings.redis_url,
            password=global_settings.redis_password,
            encoding="utf-8",
            db=global_settings.redis_db,
        )

    redis = await aioredis.from_url(
        global_settings.redis_url,
        encoding="utf-8",
        db=global_settings.redis_db,
    )

    return redis
