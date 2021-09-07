from typing import List, Optional

from pydantic import BaseModel, Field as PydanticField
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


class CreateClientBody(BaseModel):
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



class Type(BaseModel):
    name: Optional[bool] = False
    last_name: Optional[bool] = False
    full_name: Optional[bool] = False
    email: Optional[bool] = False
    booking_id : Optional[bool] = False
    phone_number: Optional[bool] = False

class TypeObject(BaseModel):
    name: Optional[Type]

class Constrain(BaseModel):
    contain: Optional[bool] = False
    equal_to: Optional[bool] = False
    starts_by: Optional[bool] = False
    ends_by: Optional[bool] = False

class ConstrainObject(BaseModel):
    name: Optional[Constrain]

class ClientSearchBody(BaseModel):
    type: Optional[TypeObject]
    constrain: Optional[ConstrainObject]
    item: Optional[str]
    
