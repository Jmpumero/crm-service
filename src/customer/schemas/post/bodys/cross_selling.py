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


class Product(BaseModel):
    id: str = Field(default_factory=PyObjectId, alias="_id")
    name: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class CrossSelling(BaseModel):
    id: str = Field(default_factory=PyObjectId, alias="_id")
    principal_product: Product
    secondary_product: Product

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class NewCrossSelling(BaseModel):
    news_cross_selling: List[CrossSelling]
