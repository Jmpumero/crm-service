from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field

from src.segmenter.schemas.get.response import segment


class StatusSegment(Enum):
    status_draft = "draft"
    status_in_progress = "in_progress"
    status_active = "active"
    status_inactive = "inactive"


class DateRange(BaseModel):
    from_: Optional[int]
    to: Optional[int]


class IntNumericRange(BaseModel):
    from_: int = Field(alias="from")
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
    # register_date: Optional[DateWithConditions]
    birth_date: Optional[DateWithConditions]
    languages: Optional[List[str]]


class UpdatedSegment(BaseModel):
    name: str
    author: str
    date_range: DateRange
    # datetime_range: Optional[DateRange]
    group_by: str
    time: Optional[str]
    applied_filters: Optional[list[AppliedFilters]]

    class Config:
        allow_population_by_field_name = True
        extra = "forbid"


class UpdateStatusSegment(BaseModel):
    status: str
