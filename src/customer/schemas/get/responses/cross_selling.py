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
    id: str
    principal_product: Product
    secondary_product: Product


class CrossSellingAndProductsResponse(BaseModel):
    products: List[Product]
    cross_selling: List[CrossSelling]
    total_cross_selling_items: Optional[int]
    total_cross_selling_show: Optional[int]
