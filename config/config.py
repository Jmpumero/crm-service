import logging
import os
from dotenv import load_dotenv

from pydantic import BaseSettings

log = logging.getLogger("uvicorn")
load_dotenv()


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")

    api_base_url: str = os.getenv("BASE_URL", "http://localhost:8000")

    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://127.0.0.1:27017/")

    redis_url: str = os.environ.get("REDIS_URL", "redis://localhost:6379")
    redis_password: str = os.getenv("REDIS_PASSWORD", "")
    redis_db: int = int(os.getenv("REDIS_DB", "0"))

    sqlite_url: str = os.getenv("SQLITE_URL", "sqlite:///./users.db")

    output_json: str = os.getenv("OUTPUT_JSON", "./clients.json")
    pagination_limit: int = int(os.getenv("PAGINATION_LIMIT", 25))

    keycloack_server_url: str = os.getenv("KEYCLOACK_SERVER_URL", "")
    keycloack_client_id: str = os.getenv("KEYCLOACK_CLIENT_ID", "")
    keycloack_client_secrect_key: str = os.getenv("KEYCLOACK_CLIENT_SECRECT_KEY", "")
    keycloack_realm_name: str = os.getenv("KEYCLOACK_REALM_NAME", "")
