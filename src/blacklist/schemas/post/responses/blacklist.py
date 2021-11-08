from typing import List, Optional

from pydantic import BaseModel


class BlackListBodyResponse(BaseModel):
    msg: str
    code: int
