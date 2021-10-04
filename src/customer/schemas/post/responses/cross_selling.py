from typing import List, Optional

from pydantic import BaseModel


class CreatedGeneralResponse(BaseModel):
    msg: str
    code: int
