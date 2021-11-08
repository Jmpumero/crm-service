from typing import Any, List, Optional
from pydantic import BaseModel
from typing_extensions import TypedDict

from pydantic import BaseModel, Field
from bson import ObjectId


class DateRange(BaseModel):
    from_: str = Field(..., alias="from")
    to: str


class DateWithConditions(BaseModel):
    date: Optional[str]
    condition: str
    date_range: Optional[DateRange]


class AppliedFilters(BaseModel):
    filter_name: str
    gender: Optional[str]
    civil_status: Optional[str]
    age_range: Optional[DateRange]
    profession: Optional[str]
    childrens: Optional[int]
    nationality: Optional[str]
    register_date: Optional[DateWithConditions]
    birth_date: Optional[DateWithConditions]
    languages: Optional[List[str]]


class Segmenter(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    author: str
    filter: Optional[str]
    status: str
    clients: int
    tags: List[str]
    date_range: DateRange
    datetime_range: Optional[DateRange]
    group_by: str
    time: Optional[str]
    applied_filters: Optional[list[AppliedFilters]]
    updated_at: str
    created_at: str
    deleted_at: str

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
