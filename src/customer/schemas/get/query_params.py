from typing import Optional
from fastapi.param_functions import Query

from pydantic import BaseModel


class SearchCustomersQueryParams(BaseModel):
    query: Optional[str] = ""
    column_name: str = "name"
    contain: str = ""
    skip: int = 0
    limit: int = 10

    order: Optional[str] = ""
    column_order: Optional[str] = ""


class BlacklistQueryParams(BaseModel):
    skip: int = 0
    limit: int = 10
    query: str = "disable"


class CustomerQueryParamsSensor(BaseModel):
    skip: int = 0
    limit: int = 10
    sensor: str


class SearchCrudQueryParams(BaseModel):
    query: str = ""
    skip: int = 0
    limit: int = 10
    column_sort: Optional[str] = "name"
    order: Optional[str] = "asc"
