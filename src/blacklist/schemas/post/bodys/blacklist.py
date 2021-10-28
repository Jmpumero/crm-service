from typing import List, Optional

from pydantic import BaseModel


class BlackListBody(BaseModel):
    id: str
    blacklist_status: bool = False
    motives: List[str]
