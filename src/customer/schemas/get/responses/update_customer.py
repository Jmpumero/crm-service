from typing import List, Optional
from pydantic import BaseModel, Field

from pydantic import BaseModel


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


class SearchUpdate(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    last_name: str
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
    language: Optional[List[Languages]]
    signature: Optional[str]
    social_media: Optional[List[SocialMedia]]
    customer_avatar: Optional[str]
    customer_status: Optional[bool]
    country: Optional[str] = None
    city: Optional[str]
    postalCode: Optional[str]
    associated_sensors: Optional[List[str]]
    blacklist_enable_motive: Optional[List[str]]
    blacklist_disable_motive: Optional[List[str]]

    # class Config:
    #     allow_population_by_field_name = True
    #     arbitrary_types_allowed = True
    #     json_encoders = {ObjectId: str}


class SearchUpdateResponse(BaseModel):
    customers: List[SearchUpdate]
    total_items: int
    total_show: int
