from typing import AsyncGenerator, Any
import aioredis
import logging

from config import config

global_settings = config.Settings()


async def get_redis() -> AsyncGenerator[Any, Any]:

    if global_settings.REDIS_URL:
        redis: aioredis.Redis = await aioredis.from_url(
            global_settings.REDIS_URL,
            password=global_settings.REDIS_PASSWORD,
            encoding="utf-8",
            db=global_settings.REDIS_DB,
        )

    redis: aioredis.Redis = await aioredis.from_url(
        global_settings.REDIS_URL,
        encoding="utf-8",
        db=global_settings.REDIS_DB,
    )

    logger = logging.getLogger("uvicorn")

    logger.info(f"REDIS: {global_settings.REDIS_URL}")

    try:
        yield redis
    finally:
        await redis.close()
