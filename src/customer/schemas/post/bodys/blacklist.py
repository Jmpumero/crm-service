from typing import List, Optional

from pydantic import BaseModel
from bson import ObjectId


class BlackListBody(BaseModel):
    id: str
    new_status: bool = False
    motives: List[str]
