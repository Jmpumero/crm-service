import logging
import os
from functools import lru_cache
from typing import Any

from pydantic import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")

    api_base_url: str = os.getenv("BASE_URL", "http://localhost:8000")

    redis_url: str = os.environ.get("REDIS_URL", "redis://localhost:6379")
    redis_password: str = os.getenv("REDIS_PASSWORD", "")
    redis_db: int = int(os.getenv("REDIS_DB", "0"))

    sqlite_url: str = os.environ.get("SQLITE_URL", "sqlite:///./users.db")

    pagination_limit: int = int(os.environ.get("PAGINATION_LIMIT", "25"))


# @lru_cache()
# def get_settings() -> BaseSettings:
#     log.info("Loading config settings from the environment...")
#     return Settings()
