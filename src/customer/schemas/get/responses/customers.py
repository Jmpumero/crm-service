from typing import List, Optional, Any
from pydantic import BaseModel

from pydantic import BaseModel, Field, validator
from fastapi.encoders import jsonable_encoder

from bson import ObjectId


# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid objectid")
#         return ObjectId(v)

#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(type="string")


# class Link(BaseModel):
#     href: str


# class Links(BaseModel):
#     self: Link
#     clients: Link


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
    isMain: bool


class Addresses(BaseModel):
    address: str
    isMain: bool


class SearchCustomers(BaseModel):
    id: str = Field(..., alias="_id")
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: Optional[str]
    last_name: Optional[str]
    age: Optional[int]
    email: Emails
    phone: Optional[Phones]
    address: Optional[List[Any]]
    documentId: Optional[List[DocumentID]]
    nationality: Optional[List[str]]
    civil_status: Optional[str]
    booking_id: Optional[str] = "1234rtyu345"

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


class SensorHistoryResponse(BaseModel):
    sensor_data: List[Any]
    total_items: int
    total_show: int
