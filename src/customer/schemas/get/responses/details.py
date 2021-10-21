from typing import Any, List, Optional

from pydantic import BaseModel


class CustomerTermAccepted(BaseModel):
    document_url: Optional[str]
    name: Optional[str]
    description: Optional[str]


class CustomerProfileDetailResponse(BaseModel):
    most_visited_hotel: Optional[str]
    recency: Optional[int]
    email: Optional[List[str]]
    phone: Optional[List[str]]
    social_networks: Optional[List[Any]]
    accepted_terms: Optional[List[CustomerTermAccepted]]
    interests: Optional[List[str]]
    communication_methods: Optional[Any]
