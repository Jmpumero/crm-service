from typing import Optional

from pydantic import BaseModel


class SearchCustomersQueryParams(BaseModel):
    query: Optional[str] = None
    column_name: str = ""
    contain: str = ""
