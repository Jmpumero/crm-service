from typing import Any, List, Optional

from typing_extensions import TypedDict

from pydantic import BaseModel, Field
from bson import ObjectId
from enum import Enum


class GenericResponse(BaseModel):
    code: int
    msg: str


class DateRange(BaseModel):
    from_: str
    to: str


class IntNumericRange(BaseModel):
    from_: int
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
    date_range: Optional[DateRange]
    group_by: Optional[str]
    time: Optional[str]
    clients: Optional[int]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class FilterResponse(BaseModel):
    client: int
