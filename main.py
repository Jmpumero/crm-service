from __future__ import annotations

from fastapi import FastAPI, Depends, status
from fastapi.security.api_key import APIKey
from fastapi.exceptions import RequestValidationError

from config import Settings

from core.security.api_key import get_api_key
from core.redis.pool_connection import init_redis_pool
from core.redis.repository import RedisRepository

from error_handlers.schemas.unauthorized import UnauthorizedError
from error_handlers import validation_error, bad_gateway, bad_request, unauthorized

from utils.remove_422 import remove_422s

from src import customers_router

global_settings = Settings()

app = FastAPI()

app.include_router(customers_router)
# app.include_router(sensor_router)  #para incluir rutas

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
    app.state.redis.close()
    await app.state.redis.wait_closed()


@app.get(
    "/secure-endpoint",
    tags=["test"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthorizedError},
    },
)
async def get_open_api_endpoint(
    api_key: APIKey = Depends(get_api_key),
) -> dict[str, str]:
    response = {"message": "you are accessing a route protected by api key"}

    return response


remove_422s(app)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {
        "Hello": "World"
    }  # cuenta la leyenda que si borras el hola mundo te ira mal el resto del proyecto
