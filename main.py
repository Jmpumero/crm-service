from __future__ import annotations
import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from config import Settings
from core import get_openapi_router
from core import on_startup, on_shutdown
from error_handlers import validation_error, bad_gateway, bad_request, unauthorized
from utils.remove_422 import remove_422s
from src.customer.controller import customers_router
from src.customer.profile_sensors_endpoint.controller import sensor_router


global_settings = Settings()

app = FastAPI(
    docs_url=None, redoc_url=None, on_startup=[on_startup], on_shutdown=[on_shutdown]
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(sensor_router)
app.include_router(customers_router)
app.include_router(get_openapi_router(app))

app.add_exception_handler(RequestValidationError, validation_error.handler)
app.add_exception_handler(bad_gateway.BadGatewayException, bad_gateway.handler)
app.add_exception_handler(bad_request.BadRequestException, bad_request.handler)
app.add_exception_handler(unauthorized.UnauthorizedException, unauthorized.handler)

logger = logging.getLogger("uvicorn")

remove_422s(app)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {
        "Hello": "World"
    }  # cuenta la leyenda que si borras el hola mundo te ira mal el resto del proyecto


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=3002, reload=True, debug=True)
