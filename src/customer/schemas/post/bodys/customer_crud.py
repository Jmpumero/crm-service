from typing import List, Optional
from fastapi.openapi.models import Link

from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


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


class SocialNetwork(BaseModel):
    name: str
    link: Optional[str]


class CreateCustomerBody(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    last_name: str
    full_name: Optional[str]
    nationality: List[str]
    phone: List[Phones]
    address: List[str]
    postal_address: str
    email: List[Emails]
    documentId: List[DocumentID]
    civil_status: str
    age: int
    birthdate: str
    language: List[Languages]
    signature: Optional[str]
    social_network: Optional[List[SocialNetwork]]
    customer_avatar: Optional[str]
    customer_status: bool = True
    blacklist_status: bool = False

    country: Optional[str] = None
    city: Optional[str]
    postalCode: Optional[str]
    associated_sensors: Optional[List[str]]
    blacklist_enable_motive: Optional[List[str]]
    blacklist_disable_motive: Optional[List[str]]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
