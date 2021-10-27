from typing import Any, List, Optional

from pydantic import BaseModel


class CrossSellingCreatedResponse(BaseModel):
    msg: str
    code: int
    details: Optional[Any] = ""
