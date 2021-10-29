from typing import List, Optional

from pydantic import BaseModel


class BlackListUpdate(BaseModel):
    id: str
    new_status: bool
    motives: List[str]


class BlacklistUpdateResponse(BaseModel):
    message: Optional[str]
    code: int
