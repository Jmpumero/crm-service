import logging
from typing import Any

from ..connection.connection import ConnectionMongo
from ..redis import RedisRepository, init_redis_pool


logger = logging.getLogger("uvicorn")


startup_result: Any = {"mongo_connection": None, "redis_connection": None}


async def on_startup():
    global startup_dict

    startup_result["mongo_connection"] = ConnectionMongo()
    startup_result["redis_connection"] = await init_redis_pool()
    startup_result["redis_repository"] = RedisRepository(
        startup_result["redis_connection"]
    )

    logger.info("startup method executed correctly")


async def on_shutdown():
    logger.info("shutdown method executed correctly")
