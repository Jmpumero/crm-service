from fastapi import APIRouter, Depends

from core import keycloack_guard
from ..schemas import (
    CustomerProfileHeaderResponse,
    CustomerProfileDetailResponse,
    CustomerLogBook,
    CustomerMarketingSubscriptions,
    PDResponse,
)
from ..services import (
    ProfileHeaderService,
    ProfileDetailService,
    MarketingSubscriptionsService,
)
from http_exceptions import NotFoundError
from ..service import Service
from utils.remove_422 import remove_422


customers_profile_router: APIRouter = APIRouter(
    tags=["Customer Profile"], dependencies=[Depends(keycloack_guard)]
)


@customers_profile_router.get(
    "/customers/{customer_id}/profile-header",
    responses={404: {"model": NotFoundError}},
    response_model=CustomerProfileHeaderResponse,
    response_model_exclude_none=True,
)
@remove_422
async def get_customer_profile_header(customer_id: str):
    service = ProfileHeaderService()

    return await service.get_profile_header(customer_id)


@customers_profile_router.get(
    "/customers/{customer_id}/details",
    response_model=PDResponse,
    response_model_exclude_none=True,
)
@remove_422
async def get_customer_profile_detail(customer_id: str):
    service = ProfileDetailService()

    return await service.get_profile_details(customer_id)


# @customers_profile_router.get(
#     "/customers/{customer_id}/details/modal-info",
# )
# @remove_422
# async def get_contact_modal_info(customer_id: str):
#     service = ProfileDetailService()

#     return await service.get_contact_modal_info(customer_id)


@customers_profile_router.get(
    "/customers/{customer_id}/logbook", response_model=CustomerLogBook
)
@remove_422
async def get_customer_logbook(customer_id: str):
    service = Service()

    return service.get_customer_logbook(customer_id)


@customers_profile_router.get(
    "/customers/{customer_id}/marketing-subscriptions",
    response_model=CustomerMarketingSubscriptions,
    response_model_exclude_none=True,
)
@remove_422
async def get_customer_marketing_subscriptions(customer_id: str):
    service = MarketingSubscriptionsService()

    return await service.get_customer_marketing_subscriptions(customer_id)
