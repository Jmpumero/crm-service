from typing import List, Optional
from pydantic import BaseModel


class CreateSegment(BaseModel):
    segment_name: str
    author: str
    # applied_filters: Optional[List]

    class Config:
        extra = "forbid"
