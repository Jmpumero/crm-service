from __future__ import annotations
from aioredis.client import Redis
from typing import Any, List, Optional

from fastapi import APIRouter, Depends
from fastapi.param_functions import Query

from src.customer.schemas.post.bodys.blacklist import BlackListBody
from src.customer.schemas.post.bodys.blacklist import BlackListBody
from core import keycloack_guard
from core import get_redis
from src.blacklist.service import BlacklistService
from src.blacklist.schemas import (
    BlacklistQueryParams,
    BlacklistResponse,
    StatusInBlacklist,
)
from utils.remove_422 import remove_422

blacklist_router = APIRouter(
    tags=["Blacklist"], dependencies=[Depends(keycloack_guard)]
)


@blacklist_router.get(
    "/blacklist/",
    response_model=BlacklistResponse,
    response_model_exclude_none=True,
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


# @blacklist_router.put(
#     "/blacklist/update/customer_id/2", response_model=BlackListBodyResponse
# )
# @remove_422
# async def update_customer_in_blacklist(body: BlackListBody):

#     service = BlacklistService()
#     return await service.post_blacklist_update_customer(body)
