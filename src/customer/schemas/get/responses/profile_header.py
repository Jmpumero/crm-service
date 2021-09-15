from typing import List

from pydantic import BaseModel


class CustomerProfileHeaderResponse(BaseModel):
    id_: str
    name: str
    score: int
    languages: List[str]
    country: str
    membership: str
    gender: str
    age: int
    next_hotel_stay: str
    next_stay_date: str
    last_checkout_date: str
    last_stay_hotel: str
    total_stays: int
    days_since_last_stay: str
    lifetime_expenses: int
    total_lodging_expenses: int
    miscellaneous_expenses: int
    average_expenditure_per_stay: int
    average_days_before_booking: int
