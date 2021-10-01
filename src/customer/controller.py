from __future__ import annotations
from src.customer.schemas.post.responses.customer_crud import CustomerCRUDResponse
from src.customer.schemas.post.bodys.blacklist import BlackListBody

# from src.customer.schemas.get.query_params import CustomerQueryParamsSensor
from config.config import Settings

from fastapi import APIRouter, Depends

from core import keycloack_guard
from .service import Service

from .schemas import (
    BlackListBodyResponse,
    SearchCustomersQueryParams,
    BlacklistQueryParams,
    CreateCustomerBody,
    CustomerCRUDResponse,
    SearchCrudQueryParams,
    UpdateCustomerBody,
    CustomerQueryParamsSensor,
    SensorHistoryResponse,
    MergeCustomerBody,
    SearchUpdate,
    SearchMergeResponse,
    SearchMerge,
)

from utils.remove_422 import remove_422

from error_handlers.schemas.validation_error import CustomValidationError
from error_handlers.schemas.bad_gateway import BadGatewayError
from error_handlers.schemas.unauthorized import UnauthorizedError
from fastapi import HTTPException

global_settings = Settings()

customers_router = APIRouter(tags=["Customers"])
# tags=["Customers"], dependencies=[Depends(keycloack_guard)]


@customers_router.get("/customers/")
@remove_422
async def get_customers(
    query_params: SearchCustomersQueryParams = Depends(SearchCustomersQueryParams),
):
    service = Service()

    return await service.get_customers(query_params)


@customers_router.get("/blacklist/")
@remove_422
async def get_customers(
    query_params: BlacklistQueryParams = Depends(BlacklistQueryParams),
):
    service = Service()

    return await service.get_customers_blacklist(query_params)


# enpoint que optiene el historial de un sensor del customer (para las tablas blacklist/crud)
@customers_router.get("/customer/{customer_id}/history-sensor")
@remove_422
async def get_customer_sensor(
    customer_id: str,
    query_params: CustomerQueryParamsSensor = Depends(CustomerQueryParamsSensor),
):
    service = Service()

    response = await service.get_history_sensor(customer_id, query_params)
    return SensorHistoryResponse(**response)


@customers_router.get("/customers/{customer_id}/notes-comments")
@remove_422
async def get_customer_notes_comments(customer_id: str):
    service = Service()

    return service.get_customer_notes_comments(customer_id)


@customers_router.get("/customers/{customer_id}/profile-header")
@remove_422
async def get_customer_profile_header(customer_id: str):
    service = Service()

    return service.get_profile_header(customer_id)


@customers_router.get("/customers/{customer_id}/details")
@remove_422
async def get_customer_profile_detail(customer_id: str):
    service = Service()

    return service.get_profile_details(customer_id)


@customers_router.get("/customers/{customer_id}/logbook")
@remove_422
async def get_customer_logbook(customer_id: str):
    service = Service()

    return service.get_customer_logbook(customer_id)


@customers_router.get("/customers/{customer_id}/marketing-subscriptions")
@remove_422
async def get_customer_marketing_subscriptions(customer_id: str):
    service = Service()

    return service.get_customer_marketing_subscriptions(customer_id)


@customers_router.put(
    "/blacklist/update/customer", response_model=BlackListBodyResponse
)
@remove_422
async def update_customer_in_blacklist(body: BlackListBody):

    service = Service()
    return await service.post_blacklist_update_customer(body)


@customers_router.get("/customers/{customer_id}/sales-summary")
@remove_422
async def get_customer_sales_summary(customer_id: int):
    service = Service()

    return await service.get_customer_sales_summary(customer_id)


@customers_router.post("/customer/", response_model=CustomerCRUDResponse)
@remove_422
async def created_customer_crud(body: CreateCustomerBody):

    service = Service()
    return await service.post_create_customer(body)


@customers_router.get("/customers/update")
@remove_422
async def get_all_customer_in_crud(
    query_params: SearchCrudQueryParams = Depends(SearchCrudQueryParams),
):

    service = Service()
    return await service.get_all_customer_with_blacklist(query_params)


@customers_router.put("/customer/")
@remove_422
async def update_customer(
    body: UpdateCustomerBody,
):

    service = Service()
    return await service.update_customer(body)


@customers_router.delete("/customer/{customer_id}")
@remove_422
async def delete_customer(customer_id: str):

    service = Service()
    return await service.delete_customer(customer_id)


@customers_router.post("/customer/merge", response_model=CustomerCRUDResponse)
@remove_422
async def created_customer_crud(body: MergeCustomerBody):

    service = Service()
    return await service.merger_customers_with_update(body)


@customers_router.get("/merge")
@remove_422
async def get_all_customer_in_crud(
    query_params: SearchCrudQueryParams = Depends(SearchCrudQueryParams),
):

    service = Service()
    return await service.get_all_customer_with_blacklist(query_params)
