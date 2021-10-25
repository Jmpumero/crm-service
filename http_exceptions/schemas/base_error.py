from pydantic import BaseModel


class BaseError(BaseModel):
    code: int
    message: str
