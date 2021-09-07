from typing import Optional

from pydantic import BaseModel


class SearchCustomersQueryParams(BaseModel):
    query: Optional[str] = ""
    column_name: str = ""
    contrain: str = ""
