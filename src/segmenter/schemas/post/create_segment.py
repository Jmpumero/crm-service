from pydantic import BaseModel


# class Demography(BaseModel):
#     gender: Optional[str]
#     civil_status: Optional[str]
#     age_range: Optional[dict[str, str]]
#     profession: Optional[str]
#     children: Optional[int]
#     nationality: Optional[str]
#     register_date: Optional[dict[str, str]]
#     birth_date: Optional[dict[str, str]]
#     languages: Optional[List[str]]


# class Activity(BaseModel):
#     recent_activity: Optional[List[str]]
#     attributes: Optional[str]


# filters = Union[Activity, Demography]


class CreateSegment(BaseModel):
    segment_name: str

    class Config:
        extra = "forbid"
