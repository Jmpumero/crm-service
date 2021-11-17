from typing import List, Optional, Any
from enum import Enum

from pydantic import BaseModel
from pydantic.fields import Field


class TotalRevenue(BaseModel):
    pass


class FrequentRooms(BaseModel):
    pass


class MostContractedServices(BaseModel):
    pass


class AverageCheckins(BaseModel):
    pass


class MostVisitedApps(BaseModel):
    pass


class AppSuiteUsage(BaseModel):
    pass


class AppFrequency(BaseModel):
    pass


class Segment(BaseModel):
    pass


class SalesSummaryResponse(BaseModel):
    total_revenue: Optional[TotalRevenue] = Field(None)
    frequent_rooms: Optional[FrequentRooms] = Field(None)
    most_contracted_services: Optional[MostContractedServices] = Field(None)
    average_checkins: Optional[AverageCheckins] = Field(None)
    most_visited_apps: Optional[MostVisitedApps] = Field(None)
    app_suite_usage: Optional[AppSuiteUsage] = Field(None)
    app_frequency: Optional[AppFrequency] = Field(None)
    segment: Optional[Segment] = Field(None)
