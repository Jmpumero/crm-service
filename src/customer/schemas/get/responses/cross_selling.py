from typing import Any, List, Optional
from pydantic import BaseModel
from typing_extensions import TypedDict

from pydantic import BaseModel, Field
from bson import ObjectId


class Product(BaseModel):
    id: str = Field(..., alias="_id")
    name: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class CrossSelling(BaseModel):
    id_principal_product: str
    id_secondary_product: str
    name_principal_product: str
    name_secondary_product: str


class CrossSellingResponse(BaseModel):
    products: List[Product]
    cross_selling: List[CrossSelling]
    total_items: int
    total_show: int
