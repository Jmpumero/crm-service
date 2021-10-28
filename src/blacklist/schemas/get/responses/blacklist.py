from typing import Any, List, Optional
from pydantic import BaseModel
from typing_extensions import TypedDict

from pydantic import BaseModel, Field
from bson import ObjectId


class DocumentID(BaseModel):
    documentType: str
    documentNumber: str


class Phones(BaseModel):
    local_format: Optional[str]
    intl_format: str
    areaCode: Optional[str]
    countryCode: Optional[str]
    isMain: bool


class Emails(BaseModel):
    email: str
    isMain: bool


class Languages(BaseModel):
    language: str
    isMain: bool


class Addresses(BaseModel):
    address: str
    isMain: bool


class BlacklistCustomer(BaseModel):
    id: str = Field(..., alias="_id")
    name: Optional[str]
    last_name: Optional[str]
    age: Optional[int]
    email: Optional[List[Emails]] = ""
    phone: Optional[List[Phones]] = ""
    address: Optional[List[Addresses]] = ""
    documentId: Optional[List[DocumentID]]
    nationality: Optional[List[str]]
    civil_status: Optional[str]
    languages: Optional[List[Languages]]
    birthdate: Optional[str]
    associated_sensors: Optional[List[str]]
    blacklist_status: bool
    blacklist_enable_motive: List[str]
    blacklist_disable_motive: List[str]
    stenant: Optional[Any]
    email_main: Optional[Emails] = ""
    phone_main: Optional[Phones] = ""
    address_main: Optional[Addresses] = ""

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class BlacklistCustomersResponse(BaseModel):
    total_items: int
    total_show: int
    items: List[BlacklistCustomer]
