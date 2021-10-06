from typing import Any, List, Optional
from pydantic import BaseModel
from typing_extensions import TypedDict

from pydantic import BaseModel, Field
from bson import ObjectId


class Segmenter(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    author: str
    filter: str
    status: str
    updated_at: str
    created_at: str
    deleted_at: str
    clients: int
    tags: List[str]
    date_from: Optional[str]
    date_to: Optional[str]
    applied_filters: Any

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class SegmenterResponse(BaseModel):
    segmenters: List[Segmenter]
    tag_list: List[str]
    total_items: int
    total_show: int
