from typing import List, Optional, Any
from enum import Enum

from pydantic import BaseModel
from pydantic.fields import Field


class Forecasts(BaseModel):
    concept: Optional[str]
    count: Optional[int]
    net_amount: Optional[float]
    avg_income: Optional[float]


class TotalRevenue(BaseModel):
    upsellings: float
    food_beverages: float
    accomodation: float


class FrequentRooms(BaseModel):
    room_name: Any
    count: int


class MostContractedServices(BaseModel):
    pass


class AverageCheckins(BaseModel):
    completed: int
    non_completed: int


class MostVisitedApps(BaseModel):
    app_name: str
    visit_count: int


class AppSuiteUsage(BaseModel):
    pass


class AppFrequency(BaseModel):
    pass


class Segment(BaseModel):
    pass


class SalesSummaryResponse(BaseModel):
    total_revenue: Optional[TotalRevenue]
    frequent_rooms: Optional[List[FrequentRooms]]
    most_contracted_services: Optional[MostContractedServices] = Field(None)
    average_checkins: Optional[AverageCheckins] = Field(None)
    most_visited_apps: Optional[List[MostVisitedApps]]
    app_suite_usage: Optional[AppSuiteUsage] = Field(None)
    app_frequency: Optional[AppFrequency] = Field(None)
    segment: Optional[Segment] = Field(None)
