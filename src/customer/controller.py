from __future__ import annotations
from config.config import Settings

from fastapi import APIRouter, status, Depends

from .service import Service

from .schemas import SearchCustomersQueryParams

from utils.remove_422 import remove_422

from error_handlers.schemas.validation_error import CustomValidationError
from error_handlers.schemas.bad_gateway import BadGatewayError
from error_handlers.schemas.unauthorized import UnauthorizedError


global_settings = Settings()

customers_router = APIRouter(
    tags=["Customers"],
)


@customers_router.get("/customers/")
@remove_422
async def get_customers(
    skip: int = 0,
    limit: int = global_settings.pagination_limit,
    query_params: SearchCustomersQueryParams = Depends(SearchCustomersQueryParams),
):
    service = Service()

    return await service.get_customers(skip, limit, query_params)
