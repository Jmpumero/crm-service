from typing import List, Optional
from pydantic import BaseModel


# class SearchCustomersResponse(BaseModel):
#     _id: str
#     name: str
#     last_name: str
#     age: int
#     email: str
#     phone: str
#     nationality: str
#     address: str
#     document_identification: str
#     civl_status: str


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


class SearchCustomersResponse(BaseModel):
    id: int
    name: str
    last_name: str
    full_name: str
    age: int
    birthdate: str
    documentId: List[DocumentID]
    phone: List[Phones]
    email: List[Emails]
    address: List[str]
    country: str
    city: str
    state: str
    postalCode: str
    language: List[Languages]
    marketCluster: List[str]
    status_blacklist: bool
    blacklist_enable_motive: List[str]
    blacklist_disable_motive: List[str]
    sensors: List[str]


class Metadata(BaseModel):
    TotalCustomer: int


class SearchCustomersResponseFinal(BaseModel):
    customer_container: List[SearchCustomersResponse]
    metadata: Metadata
