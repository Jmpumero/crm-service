from typing import List, Optional
from pydantic import BaseModel

from pydantic import BaseModel, Field
from bson import ObjectId


class DocumentID(BaseModel):
    documentType: str
    documentNumber: str


class Phones(BaseModel):
    local_format: str
    intl_format: str
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
    id: str = Field(..., alias="_id")
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    last_name: str
    age: int
    email: List[Emails]
    phone: List[Phones]
    address: List[str]
    documentId: List[DocumentID]
    nationality: str
    civilStatus: str
    languages: List[str]
    marital_status: str
    birthday: str
    customer_sensors: List[str]
    blacklist_status: bool

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ResponseMetaData(BaseModel):
    code: int
    message: str


class SearchCustomersResponse(BaseModel):
    customers: List[SearchCustomers]
    total_items: int
    total_show: int


class testagg(BaseModel):
    nombre: str
