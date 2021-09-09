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
    # id: int
    # full_name: str
    # birthdate: str
    # country: str
    # city: str
    # state: str
    # postalCode: str
    # language: List[Languages]
    # marketCluster: List[str]
    # status_blacklist: bool
    # blacklist_enable_motive: List[str]
    # blacklist_disable_motive: List[str]
    # sensors: List[str]


class ResponseMetaData(BaseModel):
    code: int
    message: str


# class Metadata(BaseModel):
#     response: ResponseMetaData
#     total_customers_in_collection: int


class SearchCustomersResponse(BaseModel):
    customer_container: List[SearchCustomers]
    total_items: int
    total_shown: int
