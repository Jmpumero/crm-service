from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field

from src.segmenter.schemas.get.response import segment


class DateRange(BaseModel):
    from_: Optional[int]
    to: Optional[int]


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
    birth_date: Optional[DateWithConditions]
    languages: Optional[List[str]]


class FilterSegment(BaseModel):

    name: str
    author: str
    date_range: DateRange
    # datetime_range: Optional[DateRange]
    group_by: str
    time: Optional[str]
    applied_filters: list[AppliedFilters]

    class Config:
        allow_population_by_field_name = True
        extra = "forbid"
