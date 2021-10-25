import logging

logger = logging.getLogger("uvicorn")


async def on_startup():
    logger.info("startup method executed correctly")


async def on_shutdown():
    logger.info("shutdown method executed correctly")
