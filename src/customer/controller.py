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
    # skip: int = 0,
    # limit: int = global_settings.pagination_limit,
    query_params: SearchCustomersQueryParams = Depends(SearchCustomersQueryParams),
):
    service = Service()

    return await service.get_customers(query_params)


@customers_router.get("/customers/{customer_id}/profile-header")
@remove_422
async def get_customer_profile_header(customer_id: int):
    service = Service()

    return service.get_profile_header(customer_id)


@customers_router.get("/customers/{customer_id}/details")
@remove_422
async def get_customer_profile_detail(customer_id: int):
    service = Service()

    return service.get_profile_details(customer_id)


@customers_router.get("/customers/{customer_id}/logbook")
@remove_422
async def get_customer_logbook(customer_id: int):
    service = Service()

    return service.get_customer_logbook(customer_id)


@customers_router.get("/customers/{customer_id}/marketing-subscriptions")
@remove_422
async def get_customer_marketing_subscriptions(customer_id: int):
    service = Service()

    return service.get_customer_marketing_subscriptions(customer_id)


@customers_router.get("/customers/{customer_id}/sales-summary")
@remove_422
async def get_customer_sales_summary(customer_id: int):
    service = Service()

    return service.get_customer_sales_summary(customer_id)
