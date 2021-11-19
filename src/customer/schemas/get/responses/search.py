from typing import List, Optional, Any
from pydantic import BaseModel

from pydantic import BaseModel, Field

from .customer_crud import Addresses, Languages, Emails, Phones, DocumentID


class Customer_wt_img(BaseModel):
    id: str = Field(..., alias="_id")
    name: Optional[str]
    last_name: Optional[str]
    age: Optional[int]
    email: Optional[list[Emails]]
    phone: Optional[list[Phones]]
    documentID: Optional[list[DocumentID]]
    languages: Optional[list[Languages]]
    nationality: Optional[List[str]]
    civil_status: Optional[str]
    address: Optional[List[Addresses]]


class ResponseSearch(BaseModel):
    total_items: int
    total_shows: int
    items: Optional[List[Customer_wt_img]]
