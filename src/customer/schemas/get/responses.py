from typing import Any, List

from pydantic import BaseModel


class SearchCustomersResponse(BaseModel):
    _id: str
    name: str
    last_name: str
    age: int
    email: str
    phone: str
    nationality: str
    address: str
    document_identification: str
    civl_status: str


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


class CustomerTermAccepted(BaseModel):
    document_url: str
    name: str
    description: str


class CustomerProfileDetailResponse(BaseModel):
    most_visited_hotel: str
    recency: str
    email: str
    phone: str
    social_networks: List[Any]
    accepted_terms: List[CustomerTermAccepted]
    interests: List[str]
    communication_methods: Any


class CustomerLogBook(BaseModel):
    first_contact_info: Any
    another_contacts: Any
    total_items: Any
    items_shown: Any
