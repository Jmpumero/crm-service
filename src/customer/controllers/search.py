from __future__ import annotations
from aioredis.client import Redis

# from typing import Any, List

from fastapi import APIRouter, Depends, status
from fastapi.param_functions import Query

from core import keycloack_guard
from ..services import SearchService
from utils.remove_422 import remove_422
from http_exceptions import NotFoundError

from ..schemas.get import ResponseSearch

search_customers_router = APIRouter(
    tags=["Search Customers"], dependencies=[Depends(keycloack_guard)]
)


@search_customers_router.get(
    "/search/customers/",
    response_model=ResponseSearch,
    # response_model_exclude_unset=True,
    # status_code=status.HTTP_200_OK,
)
@remove_422
async def get_customers(
    skip: int = Query(0),
    limit: int = Query(10),
    q: str = Query(None),
    order_sort: str = Query(None),
    column_sort: str = Query(None),
):
    service = SearchService()

    return await service.get_customers(skip, limit, q, order_sort, column_sort)
