from typing import Any, List, Optional
from pydantic import BaseModel
from typing_extensions import TypedDict

from pydantic import BaseModel, Field
from bson import ObjectId


class Segmenter(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    author: str
    filter: Optional[str]
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
    total_items: int
    total_shows: int
    items: Optional[List[Segmenter]]
    authors: Optional[List[str]]
    global_total_clients: int
    total_enable_clients: int
