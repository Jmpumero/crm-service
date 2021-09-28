from pydantic import BaseModel


class PutScoreCard(BaseModel):
    name: str
