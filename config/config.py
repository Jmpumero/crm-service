import os
from typing import Any

from pydantic import BaseSettings
from logging import getLogger

log = getLogger("uvicorn")


class Settings(BaseSettings):
    ENVIRONMENT: str
    BASE_URL: str

    MONGODB_URL: str

    REDIS_URL: str
    REDIS_PASSWORD: str
    REDIS_DB: int

    KEYCLOACK_SERVER_URL: str = os.getenv("KEYCLOACK_SERVER_URL", "")
    KEYCLOACK_CLIENT_ID: str = os.getenv("KEYCLOACK_CLIENT_ID", "")
    KEYCLOACK_CLIENT_SECRECT_KEY: str = os.getenv("KEYCLOACK_CLIENT_SECRECT_KEY", "")
    KEYCLOACK_REALM_NAME: str = os.getenv("KEYCLOACK_REALM_NAME", "")

    class Config:
        env_file = ".env"
