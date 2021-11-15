from pydantic import BaseModel, Field


class CreateCreativity(BaseModel):
    type_: str = Field(..., alias="type")
    name: str
    description: str
    author: str

    class Config:
        allow_population_by_field_name = True
