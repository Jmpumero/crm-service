from typing import Optional

from pydantic import BaseModel, Field


class PutScoreCard(BaseModel):
    class Config:
        extra = "allow"
