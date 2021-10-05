from __future__ import annotations
from typing import List
from src.customer.schemas.post.bodys.blacklist import BlackListBody
from src.customer.schemas.get.query_params import BlacklistQueryParamsSensor
from config.config import Settings

from fastapi import APIRouter, Depends

from core import keycloack_guard
from .service import Service
from .services import (
    ScoreCardService,
    ProfileHeaderService,
    ProfileDetailService,
    MarketingSubscriptionsService,
)
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
from utils.remove_422 import remove_422

from error_handlers.schemas.validation_error import CustomValidationError
from error_handlers.schemas.bad_gateway import BadGatewayError
from error_handlers.schemas.unauthorized import UnauthorizedError
from fastapi import HTTPException

global_settings = Settings()

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


@customers_router.get("/blacklist/")
@remove_422
async def get_customers_(
    query_params: BlacklistQueryParams = Depends(BlacklistQueryParams),
):
    service = Service()

    return await service.get_customers_blacklist(query_params)


@customers_router.get("/blacklist/{customer_id}/sensor")
@remove_422
async def get_customer_sensor(
    customer_id: str,
    query_params: BlacklistQueryParamsSensor = Depends(BlacklistQueryParamsSensor),
):
    service = Service()
    # la comentada se usara a futuro cuando se tenga data real...
    # return await service.get_blacklist_sensor(customer_id, query_params)
    return service.get_blacklist_sensor(customer_id, query_params)


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


@customers_router.post(
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


#### Score Card ####


@customers_router.get("/customers/{customer_id}/score-card")
async def get_customer_score_card(customer_id: str):
    service = ScoreCardService()

    return await service.get_customer_score_card(customer_id)


@customers_router.put("/customers/{customer_id}/score-card")
async def post_customer_score_card(customer_id: str, score_card: List[PutScoreCard]):
    service = ScoreCardService()

    return await service.put_score_card(customer_id, score_card)
