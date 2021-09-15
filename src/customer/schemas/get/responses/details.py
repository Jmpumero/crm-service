from typing import Any, List

from pydantic import BaseModel


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
