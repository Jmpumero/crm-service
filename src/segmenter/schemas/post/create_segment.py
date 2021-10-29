from pydantic import BaseModel


class CreateSegment(BaseModel):
    segment_name: str

    class Config:
        extra = "forbid"
