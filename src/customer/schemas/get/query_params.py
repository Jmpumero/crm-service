from typing import Optional

from pydantic import BaseModel


class SearchCustomersQueryParams(BaseModel):
    query: Optional[str] = ""
    column_name: str = ""
    contain: str = ""
    skip: int = 0
    limit: int = 10

    order: Optional[str] = ""
    column_order: Optional[str] = ""
