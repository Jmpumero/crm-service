from typing import List, Optional

from pydantic import BaseModel
from pydantic.fields import Field


class CustomerProfileHeaderResponse(BaseModel):
    id_: Optional[str] = Field(None, alias="_id")
    customer_avatar: Optional[str]
    name: Optional[str]
    last_name: Optional[str]
    score: Optional[int]
    languages: Optional[List[str]]
    country: Optional[str]
    membership: Optional[str]
    gender: Optional[str]
    age: Optional[int]
    next_hotel_stay: Optional[str]
    next_stay_date: Optional[str]
    last_checkout_date: Optional[str]
    last_stay_hotel: Optional[str]
    total_stays: Optional[int]
    total_nights: Optional[int]
    days_since_last_stay: Optional[str]
    lifetime_expenses: Optional[int]
    total_lodging_expenses: Optional[int]
    miscellaneous_expenses: Optional[int]
    average_expenditure_per_stay: Optional[int]
    average_days_before_booking: Optional[int]

    class Config:
        allow_population_by_field_name = True
