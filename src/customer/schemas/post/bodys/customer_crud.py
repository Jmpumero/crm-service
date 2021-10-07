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


class SocialMedia(BaseModel):
    name_social_media: str
    customer_social_media: str


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
    civil_status: str = ""
    age: int
    birthdate: str = ""  # format '%Y-%m-%d
    languages: List[Languages]
    signature: Optional[str]
    social_media: Optional[List[SocialMedia]] = []
    customer_avatar: Optional[str]
    customer_status: bool = True
    blacklist_status: bool = False
    associated_sensors: Optional[List[str]] = []
    country: Optional[str] = None
    city: Optional[str]
    postalCode: Optional[str]
    blacklist_enable_motive: Optional[List[str]] = []
    blacklist_disable_motive: Optional[List[str]] = []
    create_at: str = ""  # format '%Y-%m-%dT%H:%M:%S', 2021-12-31T23:59:59
    update_at: str = ""  # format '%Y-%m-%dT%H:%M:%S'
    delete_at: Optional[str] = ""  # format '%Y-%m-%dT%H:%M:%S'
    general_score: Optional[int]

    class Config:  # valida si falta un campo/campo desconocido
        extra = "forbid"

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateCustomerBody(BaseModel):
    id: str = Field(default_factory=PyObjectId, alias="_id")
    name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    nationality: Optional[List[str]]
    phone: Optional[List[Phones]]
    address: Optional[List[str]]
    postal_address: Optional[str]
    email: Optional[List[Emails]]
    documentId: Optional[List[DocumentID]]
    civil_status: Optional[str]
    age: Optional[int]
    birthdate: Optional[str]
    languages: Optional[List[Languages]]
    social_media: Optional[List[SocialMedia]]
    customer_avatar: Optional[str]
    signature: Optional[str]
    update_at: Optional[str]
    blacklist_enable_motive: Optional[List[str]] = []
    blacklist_disable_motive: Optional[List[str]] = []

    # postalCode: Optional[str]
    # country: Optional[str]
    # city: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class MergeCustomerBody(BaseModel):
    id_parent_a: str
    id_parent_b: str
    name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    nationality: Optional[List[str]]
    phone: Optional[List[Phones]]
    address: Optional[List[str]]
    postal_address: Optional[str]
    email: Optional[List[Emails]]
    documentId: List[DocumentID]
    civil_status: Optional[str]
    age: Optional[int]
    birthdate: Optional[str]
    languages: Optional[List[Languages]]
    signature: Optional[str]
    social_media: Optional[List[SocialMedia]] = []
    customer_avatar: Optional[str]
    customer_status: bool = True
    blacklist_status: Optional[bool]
    associated_sensors: Optional[List[str]] = []
    country: Optional[str] = None
    city: Optional[str]
    postalCode: Optional[str]
    blacklist_enable_motive: Optional[List[str]] = []
    blacklist_disable_motive: Optional[List[str]] = []
    create_at: Optional[str] = ""  # format '%Y-%m-%dT%H:%M:%S', 2021-12-31T23:59:59
    update_at: Optional[str] = ""  # format '%Y-%m-%dT%H:%M:%S'

    class Config:  # valida si falta un campo/campo desconocido
        extra = "forbid"
