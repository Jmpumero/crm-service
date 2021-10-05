from __future__ import annotations

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from requests.models import Request, Response

from config import Settings
from core.redis.pool_connection import init_redis_pool
from core.redis.repository import RedisRepository
from error_handlers import validation_error, bad_gateway, bad_request, unauthorized
from utils.remove_422 import remove_422s
from src import customers_router

global_settings = Settings()

app = FastAPI()

app.include_router(customers_router)

app.add_exception_handler(RequestValidationError, validation_error.handler)
app.add_exception_handler(bad_gateway.BadGatewayException, bad_gateway.handler)
app.add_exception_handler(bad_request.BadRequestException, bad_request.handler)
app.add_exception_handler(unauthorized.UnauthorizedException, unauthorized.handler)


@app.on_event("startup")
async def startup_event() -> None:
    app.state.redis = await init_redis_pool()
    app.state.redis_repo = RedisRepository(app.state.redis)


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await app.state.redis.close()
    await app.state.redis.wait_closed()


remove_422s(app)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {
        "Hello": "World"
    }  # cuenta la leyenda que si borras el hola mundo te ira mal el resto del proyecto
