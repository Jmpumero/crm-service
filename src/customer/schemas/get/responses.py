from typing import List, Optional
from pydantic import BaseModel


class ResponseMetaData(BaseModel):
    code: int
    message: str


class Link(BaseModel):
    href: str


class Links(BaseModel):
    self: Link
    clients: Link


class DocumentID(BaseModel):
    documentType: str
    documentNumber: str


class Phones(BaseModel):
    phone: str
    areaCode: str
    countryCode: str
    isMain: bool


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
    email: List[Emails]
    phone: List[Phones]
    address: List[str]
    documentId: List[DocumentID]
    nationality: str
    civilStatus: str


class ResponseMetaData(BaseModel):
    code: int
    message: str


class SearchCustomersResponse(BaseModel):
    customer_container: List[SearchCustomers]
    total_items: int
    total_shown: int
