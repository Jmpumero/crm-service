from typing import List, Optional, Any
from pydantic import BaseModel, Field

from pydantic import BaseModel


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


class SocialMedia(BaseModel):
    name_social_media: str
    customer_social_media: str


class Addresses(BaseModel):
    address: str
    isMain: bool


class BlacklistLog(BaseModel):
    date: str
    motives: List[str]
    type: str


class SearchUpdate(BaseModel):
    id: str = Field(..., alias="_id")
    name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    nationality: Optional[List[str]]
    phone: Optional[List[Phones]]
    address: Optional[List[Addresses]]
    postal_address: Optional[str]
    email: Optional[List[Emails]]
    documentId: Optional[List[DocumentID]]
    civil_status: Optional[str]
    age: Optional[int]
    birthdate: Optional[str]
    languages: Optional[List[Languages]]
    signature: Optional[str]
    social_media: Optional[List[SocialMedia]]
    customer_avatar: Optional[str]
    customer_status: Optional[bool]
    country: Optional[str] = None
    city: Optional[str]
    postalCode: Optional[str]
    associated_sensors: Optional[List[str]]
    blacklist_last_enabled_motive: Optional[List[str]]
    blacklist_last_disabled_motive: Optional[List[str]]
    blacklist_status: Optional[bool]
    stenant: Optional[Any]
    gender: Optional[str]
    profession: Optional[str]
    total_childrens: Optional[int]
    blacklist_log: Optional[List[BlacklistLog]]
    # class Config:
    #     allow_population_by_field_name = True
    #     arbitrary_types_allowed = True
    #     json_encoders = {ObjectId: str}


class SearchUpdateResponse(BaseModel):
    customers: List[SearchUpdate]
    total_items: int
    total_show: int


class SearchMerge(BaseModel):

    name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    nationality: Optional[List[str]]
    phone: Optional[List[Phones]]
    address: Optional[List[Addresses]]
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
    blacklist_status: Optional[bool] = False
    associated_sensors: Optional[List[str]] = []
    country: Optional[str] = None
    city: Optional[str]
    postalCode: Optional[str]
    blacklist_last_enabled_motive: Optional[List[str]] = []
    blacklist_last_disabled_motive: Optional[List[str]] = []
    create_at: Optional[str] = ""  # format '%Y-%m-%dT%H:%M:%S', 2021-12-31T23:59:59
    update_at: Optional[str] = ""  # format '%Y-%m-%dT%H:%M:%S'
    stenant: Optional[Any] = None
    gender: Optional[str]
    profession: Optional[str]
    total_childrens: Optional[int]
    blacklist_log: Optional[List[BlacklistLog]]


class SearchMergeResponse(BaseModel):
    customers: List[SearchMerge]
    total_items: int
    total_show: int
