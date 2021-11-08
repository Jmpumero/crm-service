from pydantic import BaseModel


class CreateSegment(BaseModel):
    segment_name: str
    author: str

    class Config:
        extra = "forbid"
