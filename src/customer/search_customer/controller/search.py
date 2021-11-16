from __future__ import annotations
from aioredis.client import Redis
from typing import Any, List

from fastapi import APIRouter, Depends

from src.customer.schemas.post.responses.customer_crud import CustomerCRUDResponse
from src.customer.schemas.post.bodys.blacklist import BlackListBody
from src.customer.schemas.post.bodys.blacklist import BlackListBody
from core import keycloack_guard


from ...schemas import SearchCustomersQueryParams, BlacklistQueryParams
from ...schemas import BlackListBodyResponse
from ...schemas import (
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
    tags=["Search Customers"], dependencies=[Depends(keycloack_guard)]
)
