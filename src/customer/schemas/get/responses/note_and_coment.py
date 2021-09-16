from typing import List, Optional
from pydantic import BaseModel


class Link(BaseModel):
    href: str


class Links(BaseModel):
    self: Link
    clients: Link


class Emails(BaseModel):
    email: str
    isMain: bool


class Languages(BaseModel):
    language: str
    is_main: bool


class SearchCustomers(BaseModel):
    name: str
    last_name: str
    age: int
    email: Emails

    address: List[str]

    nationality: str
    civilStatus: str
    booking_id: str


class ResponseMetaData(BaseModel):
    code: int
    message: str


class SearchCustomersResponse(BaseModel):
    customers: List[SearchCustomers]
    total_items: int
    total_show: int


class testagg(BaseModel):
    nombre: str
