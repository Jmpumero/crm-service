from pydantic import BaseModel


class ApiKeyPayload(BaseModel):
    aplication_name: str
