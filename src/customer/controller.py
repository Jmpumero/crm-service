from __future__ import annotations
from typing import List
from src.customer.schemas.post.responses.customer_crud import CustomerCRUDResponse
from typing import Any, List
from src.customer.schemas.post.bodys.blacklist import BlackListBody

from config.config import Settings

from fastapi import APIRouter, Depends

from src.customer.schemas.post.bodys.blacklist import BlackListBody

from config.config import Settings
from core import keycloack_guard
from .service import Service
from .services import (
    ScoreCardService,
    ProfileHeaderService,
    ProfileDetailService,
    MarketingSubscriptionsService,
)
from .schemas import SearchCustomersQueryParams, PutScoreCard

from .schemas import SearchCustomersQueryParams
from .schemas import PutScoreCard
from .schemas import (
    SearchCustomersQueryParams,
    PutScoreCard,
    CustomerProfileHeaderResponse,
    CustomerProfileDetailResponse,
    CustomerLogBook,
    CustomerMarketingSubscriptions,
)

from .schemas import SearchCustomersQueryParams, BlacklistQueryParams
from .schemas import BlackListBodyResponse

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
    CrossSellingCreatedResponse,
    SearchUpdate,
    SearchMergeResponse,
    SearchMerge,
    CrossSellingQueryParams,
    CrossSelling,
    NewCrossSelling,
    Product,
    CrossSellingAndProductsResponse,
)

from utils.remove_422 import remove_422
from error_handlers.schemas.validation_error import CustomValidationError
from error_handlers.schemas.bad_gateway import BadGatewayError
from error_handlers.schemas.unauthorized import UnauthorizedError


global_settings = Settings()

customers_router = APIRouter(
    tags=["Customers"], dependencies=[Depends(keycloack_guard)]
)
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
async def get_customers_(
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


@customers_router.get(
    "/customers/{customer_id}/profile-header",
    response_model=CustomerProfileHeaderResponse,
)
@remove_422
async def get_customer_profile_header(customer_id: str):
    service = ProfileHeaderService()

    return await service.get_profile_header(customer_id)


@customers_router.get(
    "/customers/{customer_id}/details", response_model=CustomerProfileDetailResponse
)
@remove_422
async def get_customer_profile_detail(customer_id: str):
    service = ProfileDetailService()

    return await service.get_profile_details(customer_id)


@customers_router.get(
    "/customers/{customer_id}/logbook", response_model=CustomerLogBook
)
@remove_422
async def get_customer_logbook(customer_id: str):
    service = Service()

    return service.get_customer_logbook(customer_id)


@customers_router.get(
    "/customers/{customer_id}/marketing-subscriptions",
    response_model=CustomerMarketingSubscriptions,
)
@remove_422
async def get_customer_marketing_subscriptions(customer_id: str):
    service = MarketingSubscriptionsService()

    return await service.get_customer_marketing_subscriptions(customer_id)


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


@customers_router.get("/cross-selling", response_model=CrossSellingAndProductsResponse)
@remove_422
async def get_product_and_cross_selling_list(
    query_params: CrossSellingQueryParams = Depends(CrossSellingQueryParams),
):

    service = Service()
    return await service.get_product_and_cross_selling_items(query_params)


@customers_router.post(
    "/cross-selling/product", response_model=CrossSellingCreatedResponse
)
@remove_422
async def created_cross_selling_product(body: Product):

    service = Service()
    return await service.post_create_cross_selling_product(body)


@customers_router.post("/cross-selling", response_model=CrossSellingCreatedResponse)
@remove_422
async def created_cross_selling(body: NewCrossSelling):

    service = Service()

    return await service.post_create_cross_selling(body)


#### Score Card ####


@customers_router.get("/customers/{customer_id}/score-card")
@remove_422
async def get_customer_score_card(customer_id: str):
    service = ScoreCardService()

    return await service.get_customer_score_card(customer_id)


@customers_router.put("/customers/{customer_id}/score-card")
@remove_422
async def post_customer_score_card(customer_id: str, score_card: PutScoreCard):
    service = ScoreCardService()

    return await service.put_score_card(customer_id, score_card)
