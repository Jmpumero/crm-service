from __future__ import annotations
from aioredis.client import Redis
from typing import Any, List

from fastapi import APIRouter, Depends

from src.customer.schemas.post.responses.customer_crud import CustomerCRUDResponse
from src.customer.schemas.post.bodys.blacklist import BlackListBody
from src.customer.schemas.post.bodys.blacklist import BlackListBody
from core import keycloack_guard
from .service import Service
from .services import (
    ScoreCardService,
    ProfileHeaderService,
    ProfileDetailService,
    MarketingSubscriptionsService,
    SalesSummary,
    SegmenterService,
)
from core import get_redis
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
    Segmenter,
    SegmenterResponse,
    SegmenterQueryParams,
)
from utils.remove_422 import remove_422


customers_router = APIRouter(
    tags=["Customers"], dependencies=[Depends(keycloack_guard)]
)


@customers_router.get("/customers/")
@remove_422
async def get_customers(
    query_params: SearchCustomersQueryParams = Depends(SearchCustomersQueryParams),
):
    service = Service()

    return await service.get_customers(query_params)


# enpoint que optiene el historial de un sensor del customer (para las tablas blacklist/crud)
@customers_router.get(
    "/customers/{customer_id}/history-sensor",
    response_model=Any,
)
@remove_422
async def get_customer_sensor(
    customer_id: str,
    query_params: CustomerQueryParamsSensor = Depends(CustomerQueryParamsSensor),
):
    service = Service()

    response = await service.get_history_sensor(customer_id, query_params)
    return response


@customers_router.get("/customers/{customer_id}/notes-comments")
@remove_422
async def get_customer_notes_comments(customer_id: str):
    service = Service()

    return service.get_customer_notes_comments(customer_id)


##############################################################################


##############################################################################


@customers_router.get("/customers/{customer_id}/sales-summary")
@remove_422
async def get_customer_sales_summary(
    customer_id: str, redis: Redis = Depends(get_redis)
):
    service = SalesSummary()

    return await service.get_customer_sales_summary(customer_id, redis)


#### CRUD ####


@customers_router.post("/customers/", response_model=CustomerCRUDResponse)
@remove_422
async def created_customer_crud(body: CreateCustomerBody):

    service = Service()
    return await service.post_create_customer(body)


@customers_router.get("/customers/update")
@remove_422
async def get_all_customer_in_crud_update(
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


@customers_router.delete("/customer/{customer_id}", response_model=CustomerCRUDResponse)
@remove_422
async def delete_customer(customer_id: str):

    service = Service()
    return await service.delete_customer(customer_id)


@customers_router.post("/customer/merge", response_model=CustomerCRUDResponse)
@remove_422
async def created_customer_crud_(body: MergeCustomerBody):

    service = Service()
    return await service.merger_customers_with_update(body)


@customers_router.get("/merge")
@remove_422
async def get_all_customer_in_crud_merge(
    query_params: SearchCrudQueryParams = Depends(SearchCrudQueryParams),
):

    service = Service()
    return await service.get_all_customer_with_blacklist(query_params)


#### Cross Selling ####


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


@customers_router.delete("/cross-selling/{cross_selling_id}")
@remove_422
async def delete_cross_selling(cross_selling_id: str):

    service = Service()
    return await service.delete_cross_selling(cross_selling_id)


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


#### Segmenter ####
@customers_router.get("/segments", response_model=Any)
@remove_422
async def get_segmenter_list(
    query_params: SegmenterQueryParams = Depends(SegmenterQueryParams),
):

    service = SegmenterService()
    return await service.get_segmenters(query_params)


# @customers_router.get("/segmenter/authors", response_model=)
# @remove_422
# async def get_author_segments_list():

#     service = Service()
#     return await service.get_author_segments_list()
