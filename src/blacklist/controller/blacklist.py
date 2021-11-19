from __future__ import annotations
from aioredis.client import Redis
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, status, Path
from fastapi import Body, Query


from http_exceptions import BadGatewayError, UnauthorizedError, NotFoundError
from src.customer.schemas.post.bodys.blacklist import BlackListBody
from src.customer.schemas.post.bodys.blacklist import BlackListBody
from core import keycloack_guard

# from core import get_redis
from src.blacklist.service import BlacklistService
from src.blacklist.schemas import (
    BlacklistResponse,
    StatusInBlacklist,
    BlackListUpdate,
    BlacklistUpdateResponse,
)
from utils.remove_422 import remove_422

blacklist_router = APIRouter(
    tags=["Blacklist"], dependencies=[Depends(keycloack_guard)]
)


@blacklist_router.get(
    "/blacklist/",
    response_model=BlacklistResponse,
    # response_model_exclude_none=True,
)
@remove_422
async def get_customers_(
    query: Optional[str] = None,
    skip: int = Query(default=0),
    limit: int = Query(default=10),
    column_sort: Optional[str] = None,
    order_sort: Optional[str] = None,
    status: StatusInBlacklist = Query(...),
):
    service = BlacklistService()

    return await service.get_customers_blacklist(
        query, skip, limit, column_sort, order_sort, status.value
    )


@blacklist_router.get(
    "/blacklist/{id_customer}",
    # response_model=BlacklistResponse,
    response_model_exclude_none=True,
)
@remove_422
async def get_customers_(
    id_customer: str = Path(..., title="The ID of the customer to get"),
):
    service = BlacklistService()

    return await service.get_customers_blacklist(id_customer)


@blacklist_router.put(
    "/blacklist/update/customer",
    response_model=BlacklistUpdateResponse,
    response_model_exclude_unset=True,
    responses={status.HTTP_404_NOT_FOUND: {"model": NotFoundError}},
    status_code=status.HTTP_200_OK,
)
@remove_422
async def update_customer(body: BlackListUpdate = Body(...)):

    service = BlacklistService()
    return await service.update_(body)
