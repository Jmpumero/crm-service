from typing import List, Optional

from pydantic import BaseModel
from .customer_crud import Phones, Addresses, Emails, SocialMedia


class Contact(BaseModel):
    phone: List[Phones] = None
    address: List[Addresses] = None
    email: List[Emails]
    social_media: Optional[List[SocialMedia]] = None


class Hotel(BaseModel):
    most_v_hotel: str = None
    recency: int = None


class PDResponse(BaseModel):
    contact: List[Contact]
    interest: List[str] = None
    data_hotel: Optional[Hotel]
