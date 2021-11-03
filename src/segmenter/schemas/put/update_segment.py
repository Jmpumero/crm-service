from typing import List, Optional

from pydantic import BaseModel, Field


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


class UpdatedSegment(BaseModel):
    segment_id: str
    name: str
    author: str
    date_range: DateRange
    datetime_range: Optional[DateRange]
    group_by: str
    time: Optional[str]
    applied_filters: Optional[list[AppliedFilters]]

    class Config:
        allow_population_by_field_name = True
        extra = "forbid"
