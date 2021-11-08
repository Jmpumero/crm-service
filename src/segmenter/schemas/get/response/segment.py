from typing import Any, List, Optional

from typing_extensions import TypedDict

from pydantic import BaseModel, Field
from bson import ObjectId
from enum import Enum


class DateRange(BaseModel):
    from_: str = Field(..., alias="from")
    to: str


class IntNumericRange(BaseModel):
    from_: int = Field(..., alias="from")
    to: int


class DateWithConditions(BaseModel):
    date: Optional[str]
    condition: Optional[str]
    date_range: Optional[DateRange]


class AppliedFilters(BaseModel):
    filter_name: str
    gender: Optional[str]
    civil_status: Optional[str]
    age_range: Optional[IntNumericRange]
    profession: Optional[str]
    childrens: Optional[int]
    nationality: Optional[str]
    register_date: Optional[DateWithConditions]
    birth_date: Optional[DateWithConditions]
    languages: Optional[List[str]]


class SegmentDetails(BaseModel):
    id: str = Field(..., alias="_id")
    name: Optional[str]
    author: str
    create_at: str
    update_at: str
    status: str
    applied_filters: Optional[list[AppliedFilters]]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class SegmentDetailResponse(BaseModel):
    ...
