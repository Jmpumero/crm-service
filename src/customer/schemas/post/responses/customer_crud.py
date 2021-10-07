from typing import List, Optional

from pydantic import BaseModel


class CustomerCRUDResponse(BaseModel):
    msg: str
    code: int
