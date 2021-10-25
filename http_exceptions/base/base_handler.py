from typing import TypeVar, Any

from fastapi import responses
from starlette.requests import Request

from ..exceptions import UnauthorizedException, BadGatewayException, BadRequestException

HttpException = TypeVar(
    "HttpException", UnauthorizedException, BadGatewayException, BadRequestException
)


async def base_handler(
    request: Request, exception: HttpException, **kwargs: Any
) -> responses.JSONResponse:

    return responses.JSONResponse(
        status_code=exception.status_code,
        content={"message": exception.message},
    )
