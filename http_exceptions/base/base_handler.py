from typing import TypeVar

from fastapi import responses

from ..exceptions import UnauthorizedException, BadGatewayException, BadRequestException

HttpException = TypeVar(
    "HttpException", UnauthorizedException, BadGatewayException, BadRequestException
)


async def base_handler(request, exc: HttpException) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )
