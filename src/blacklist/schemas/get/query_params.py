from typing import List, Optional
from fastapi.param_functions import Query
from enum import Enum

from pydantic import BaseModel


class GenericSearch(BaseModel):
    query: Optional[str]
    columns_search: Optional[List[str]]
    skip: int = 0
    limit: int = 10
    column_sort: Optional[str] = "name"
    order_sort: Optional[str] = "asc"


class StatusInBlacklist(Enum):
    status_enable = "enable"
    status_disable = "disable"


class BlacklistQueryParams(GenericSearch):
    status: StatusInBlacklist
    query: str
